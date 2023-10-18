import json
import logging
import time
from copy import copy
from dataclasses import dataclass
from typing import Optional, Generator, Any, cast, Tuple

from . import api_support
from .completions import PromptTemplates, CompletionResponse, CompletionChunk, PromptTemplateWithMetadata, \
    ChatCompletionResponse, ChatMessage
from .errors import TemplateNotFoundError, APIKeyMissingError, AuthorizationError, FreeplayError
from .flavors import Flavor, ChatFlavor
from .llm_parameters import LLMParameters
from .provider_config import ProviderConfig

JsonDom = dict[str, Any]
Variables = dict[str, str]

logger = logging.getLogger(__name__)
default_tag = 'latest'


class CallSupport:
    def __init__(
            self,
            freeplay_api_key: str,
            api_base: str,
            **kwargs: Any
    ) -> None:
        self.api_base = api_base
        self.freeplay_api_key = freeplay_api_key
        self.client_params = LLMParameters(kwargs)

    @staticmethod
    def find_template_by_name(prompts: PromptTemplates, template_name: str) -> PromptTemplateWithMetadata:
        templates = [t for t in prompts.templates if t.name == template_name]
        if len(templates) == 0:
            raise TemplateNotFoundError(f'Could not find template with name "{template_name}"')
        return templates[0]

    def create_session(self, project_id: str, tag: str, test_run_id: Optional[str] = None) -> JsonDom:
        request_body = {'test_run_id': test_run_id} if test_run_id is not None else None
        response = api_support.post_raw(api_key=self.freeplay_api_key,
                                        url=f'{self.api_base}/projects/{project_id}/sessions/tag/{tag}',
                                        payload=request_body)

        if response.status_code == 201:
            return cast(dict[str, Any], json.loads(response.content))
        elif response.status_code == 401:
            raise AuthorizationError()
        else:
            raise FreeplayError(f'Unknown response while creating a session. Response code: {response.status_code}')

    def get_prompts(self, project_id: str, tag: str) -> PromptTemplates:
        prompts = api_support.get(
            target_type=PromptTemplates,
            api_key=self.freeplay_api_key,
            url=f'{self.api_base}/projects/{project_id}/templates/all/{tag}'
        )
        return prompts

    def prepare_and_make_chat_call(
            self,
            session_id: str,
            flavor: ChatFlavor,
            provider_config: ProviderConfig,
            tag: str,
            target_template: PromptTemplateWithMetadata,
            variables: Variables,
            message_history: list[ChatMessage],
            new_messages: Optional[list[ChatMessage]],
            test_run_id: Optional[str] = None,
            completion_parameters: Optional[LLMParameters] = None) -> ChatCompletionResponse:
        # make call
        start = time.time()
        try:
            params = target_template.get_params() \
                .merge_and_override(self.client_params) \
                .merge_and_override(completion_parameters)
            prompt_messages = copy(message_history)
            if new_messages is not None:
                prompt_messages.extend(new_messages)
            completion_response = flavor.continue_chat(messages=prompt_messages, provider_config=provider_config,
                                                       llm_parameters=params)
        except Exception as e:
            raise FreeplayError("Error calling service") from e
        end = time.time()

        model = flavor.get_model_params(params).get('model')
        formatted_prompt = json.dumps(prompt_messages)
        # record data
        self.__record_call(
            completion_response.content,
            completion_response.is_complete,
            end,
            formatted_prompt,
            session_id,
            start,
            target_template,
            variables,
            flavor.record_format_type,
            tag,
            test_run_id,
            model,
            flavor.provider,
            params
        )

        return completion_response

    def prepare_and_make_chat_call_stream(
            self,
            session_id: str,
            flavor: ChatFlavor,
            provider_config: ProviderConfig,
            tag: str,
            target_template: PromptTemplateWithMetadata,
            variables: Variables,
            message_history: list[ChatMessage],
            test_run_id: Optional[str] = None,
            completion_parameters: Optional[LLMParameters] = None
    ) -> Generator[CompletionChunk, None, None]:
        # make call
        start = time.time()
        try:
            prompt_messages = copy(message_history)
            params = target_template.get_params() \
                .merge_and_override(self.client_params) \
                .merge_and_override(completion_parameters)
            completion_response = flavor.continue_chat_stream(prompt_messages, provider_config, llm_parameters=params)
        except Exception as e:
            raise FreeplayError("Error calling service") from e
        end = time.time()

        str_content = ''
        last_is_complete = False
        for chunk in completion_response:
            str_content += chunk.text or ''
            last_is_complete = chunk.is_complete
            yield chunk

        model = flavor.get_model_params(params).get('model')
        formatted_prompt = json.dumps(prompt_messages)
        self.__record_call(
            str_content,
            last_is_complete,
            end,
            formatted_prompt,
            session_id,
            start,
            target_template,
            variables,
            flavor.record_format_type,
            tag,
            test_run_id,
            model,
            flavor.provider,
            params
        )

    def prepare_and_make_call(
            self,
            session_id: str,
            prompts: PromptTemplates,
            template_name: str,
            variables: dict[str, str],
            flavor: Optional[Flavor],
            provider_config: ProviderConfig,
            tag: str,
            test_run_id: Optional[str] = None,
            completion_parameters: Optional[LLMParameters] = None
    ) -> CompletionResponse:
        target_template = self.find_template_by_name(prompts, template_name)
        params = target_template.get_params() \
            .merge_and_override(self.client_params) \
            .merge_and_override(completion_parameters)

        final_flavor = pick_flavor_from_config(flavor, target_template.flavor_name)
        formatted_prompt = final_flavor.format(target_template, variables)

        # make call
        start = time.time()
        try:
            completion_response = final_flavor.call_service(
                formatted_prompt=formatted_prompt, provider_config=provider_config, llm_parameters=params)
        except Exception as e:
            raise FreeplayError("Error calling service") from e
        end = time.time()

        model = final_flavor.get_model_params(params).get('model')

        # record data
        self.__record_call(
            completion_response.content,
            completion_response.is_complete,
            end,
            formatted_prompt,
            session_id,
            start,
            target_template,
            variables,
            final_flavor.record_format_type,
            tag,
            test_run_id,
            model,
            final_flavor.provider,
            params
        )

        return completion_response

    def prepare_and_make_call_stream(
            self,
            session_id: str,
            prompts: PromptTemplates,
            template_name: str,
            variables: dict[str, str],
            flavor: Optional[Flavor],
            provider_config: ProviderConfig,
            tag: str,
            test_run_id: Optional[str] = None,
            completion_parameters: Optional[LLMParameters] = None
    ) -> Generator[CompletionChunk, None, None]:
        target_template = self.find_template_by_name(prompts, template_name)
        params = target_template.get_params() \
            .merge_and_override(self.client_params) \
            .merge_and_override(completion_parameters)

        final_flavor = pick_flavor_from_config(flavor, target_template.flavor_name)
        formatted_prompt = final_flavor.format(target_template, variables)

        # make call
        start = int(time.time())
        completion_response = final_flavor.call_service_stream(
            formatted_prompt=formatted_prompt, provider_config=provider_config, llm_parameters=params)
        text_chunks = []
        last_is_complete = False
        for chunk in completion_response:
            text_chunks.append(chunk.text)
            last_is_complete = chunk.is_complete
            yield chunk
        end = int(time.time())

        model = final_flavor.get_model_params(params).get('model')

        self.__record_call(''.join(text_chunks),
                           last_is_complete,
                           end,
                           formatted_prompt,
                           session_id,
                           start,
                           target_template,
                           variables,
                           final_flavor.record_format_type,
                           tag,
                           test_run_id,
                           model,
                           final_flavor.provider,
                           params)

    def __record_call(
            self,
            completion_content: str,
            completion_is_complete: bool,
            end: float,
            formatted_prompt: str,
            session_id: str,
            start: float,
            target_template: PromptTemplateWithMetadata,
            variables: dict[str, str],
            record_format_type: str,
            tag: str,
            test_run_id: Optional[str],
            model: Optional[str],
            provider: Optional[str],
            llm_parameters: Optional[LLMParameters]
    ) -> None:

        record_payload = {
            "session_id": session_id,
            "project_version_id": target_template.project_version_id,
            "prompt_template_id": target_template.prompt_template_id,
            "start_time": start,
            "end_time": end,
            "tag": tag,
            "inputs": variables,
            "prompt_content": formatted_prompt,
            "return_content": completion_content,
            "format_type": record_format_type,
            "is_complete": completion_is_complete,
            "model": model,
            "provider": provider,
            "llm_parameters": llm_parameters
        }

        if test_run_id is not None:
            record_payload['test_run_id'] = test_run_id

        try:
            recorded_response = api_support.post_raw(
                api_key=self.freeplay_api_key,
                url=f'{self.api_base}/v1/record',
                payload=record_payload
            )
            recorded_response.raise_for_status()
        except Exception as e:
            status_code = -1
            if hasattr(e, 'response') and hasattr(e.response, 'status_code'):
                status_code = e.response.status_code
            logger.warning(f'There was an error recording to Freeplay. Call will not be logged. '
                           f'Status: {status_code}. {e.__class__}')


class Session:
    def __init__(
            self,
            call_support: CallSupport,
            session_id: str,
            prompts: PromptTemplates,
            flavor: Optional[Flavor],
            provider_config: ProviderConfig,
            tag: str = default_tag,
            test_run_id: Optional[str] = None
    ) -> None:
        self.tag = tag
        self.call_support = call_support
        self.session_flavor = flavor
        self.provider_config = provider_config
        self.session_id = session_id
        self.prompts = prompts
        self.test_run_id = test_run_id

    def get_completion(
            self,
            template_name: str,
            variables: dict[str, str],
            flavor: Optional[Flavor] = None,
            **kwargs: Any
    ) -> CompletionResponse:
        completion_flavor = flavor or self.session_flavor
        return self.call_support.prepare_and_make_call(self.session_id,
                                                       self.prompts,
                                                       template_name,
                                                       variables,
                                                       completion_flavor,
                                                       self.provider_config,
                                                       self.tag,
                                                       self.test_run_id,
                                                       completion_parameters=LLMParameters(kwargs))

    def get_completion_stream(
            self,
            template_name: str,
            variables: dict[str, str],
            flavor: Optional[Flavor] = None,
            **kwargs: Any
    ) -> Generator[CompletionChunk, None, None]:
        completion_flavor = flavor or self.session_flavor
        return self.call_support.prepare_and_make_call_stream(self.session_id,
                                                              self.prompts,
                                                              template_name,
                                                              variables,
                                                              completion_flavor,
                                                              self.provider_config,
                                                              self.tag,
                                                              self.test_run_id,
                                                              completion_parameters=LLMParameters(kwargs))


class ChatSession(Session):
    def __init__(
            self,
            call_support: CallSupport,
            session_id: str,
            prompts: PromptTemplates,
            flavor: Optional[ChatFlavor],
            provider_config: ProviderConfig,
            template_name: str,
            variables: Variables,
            tag: str = default_tag,
            test_run_id: Optional[str] = None,
            messages: Optional[list[ChatMessage]] = None
    ) -> None:
        super().__init__(call_support, session_id, prompts, flavor, provider_config, tag, test_run_id)
        # A Chat Session tracks the template_name and variables for a set of chat completions.
        # Assumes these will be the same for subsequent chat messages.
        self.message_history = messages or []
        self.variables = variables
        self.target_template = self.call_support.find_template_by_name(self.prompts, template_name)
        self.flavor = get_chat_flavor_from_config(flavor, self.target_template.flavor_name)
        self.__initial_messages = json.loads(self.flavor.format(self.target_template, self.variables))

    def last_message(self) -> Optional[ChatMessage]:
        return self.message_history[len(self.message_history) - 1]

    def store_new_messages(self, new_messages: list[ChatMessage]) -> None:
        for message in new_messages:
            self.message_history.append({
                "role": message["role"],
                "content": message["content"]
            })

    def start_chat(self, **kwargs: Any) -> ChatCompletionResponse:
        response = self.call_support.prepare_and_make_chat_call(
            self.session_id,
            flavor=self.flavor,
            provider_config=self.provider_config,
            tag=self.tag,
            test_run_id=self.test_run_id,
            target_template=self.target_template,
            variables=self.variables,
            message_history=self.__initial_messages,
            new_messages=None,
            completion_parameters=LLMParameters(kwargs)
        )

        self.store_new_messages(response.message_history)
        return response

    def start_chat_stream(self, **kwargs: Any) -> Generator[CompletionChunk, None, None]:
        return self.continue_chat_stream(new_messages=None, **kwargs)

    def aggregate_message_from_response(self, response: Generator[CompletionChunk, None, None]) -> Generator[
        CompletionChunk, Any, None]:
        message: ChatMessage = {
            "role": "assistant",
            "content": ""
        }

        for chunk in response:
            message["content"] += chunk.text
            yield chunk

        self.message_history.append(message)

    def continue_chat(
            self,
            new_messages: Optional[list[ChatMessage]] = None,
            **kwargs: Any
    ) -> ChatCompletionResponse:

        response = self.call_support.prepare_and_make_chat_call(
            self.session_id,
            flavor=self.flavor,
            provider_config=self.provider_config,
            tag=self.tag,
            test_run_id=self.test_run_id,
            target_template=self.target_template,
            variables=self.variables,
            message_history=self.message_history,
            new_messages=new_messages,
            completion_parameters=LLMParameters(kwargs)
        )

        if new_messages is not None:
            self.store_new_messages(new_messages)
        if response.content:
            self.message_history.append(response.message_history[-1])

        return response

    def continue_chat_stream(
            self,
            new_messages: Optional[list[ChatMessage]] = None,
            **kwargs: Any
    ) -> Generator[CompletionChunk, None, None]:
        new_messages = new_messages or []
        if len(self.message_history) == 0:
            self.message_history = self.__initial_messages

        response = self.call_support.prepare_and_make_chat_call_stream(
            self.session_id,
            flavor=self.flavor,
            provider_config=self.provider_config,
            tag=self.tag,
            target_template=self.target_template,
            variables=self.variables,
            message_history=self.message_history,
            test_run_id=self.test_run_id,
            completion_parameters=LLMParameters(kwargs))

        self.store_new_messages(new_messages)
        yield from self.aggregate_message_from_response(response)


@dataclass()
class FreeplayTestRun:
    def __init__(
            self,
            call_support: CallSupport,
            flavor: Optional[Flavor],
            provider_config: ProviderConfig,
            test_run_id: str,
            inputs: list[dict[str, str]]
    ):
        self.call_support = call_support
        self.flavor = flavor
        self.provider_config = provider_config
        self.test_run_id = test_run_id
        self.inputs = inputs

    def get_inputs(self) -> list[dict[str, str]]:
        return self.inputs

    def create_session(self, project_id: str, tag: str = default_tag) -> Session:
        project_session = self.call_support.create_session(project_id, tag, self.test_run_id)
        prompts = self.call_support.get_prompts(project_id, tag)
        return Session(self.call_support, project_session['session_id'], prompts, self.flavor, self.provider_config,
                       tag, self.test_run_id)


# This SDK prototype does not support full functionality of either OpenAI's API or Freeplay's
# The simplifications are:
#  - Always assumes there is a single choice returned, does not support multiple
#  - Does not support an "escape hatch" to allow use of features we don't explicitly expose
class Freeplay:
    def __init__(
            self,
            freeplay_api_key: str,
            api_base: str,
            provider_config: ProviderConfig,
            flavor: Optional[Flavor] = None,
            **kwargs: Any
    ) -> None:
        if not freeplay_api_key or not freeplay_api_key.strip():
            raise APIKeyMissingError("Freeplay API key not set. It must be set to the Freeplay API.")
        provider_config.validate()

        self.call_support = CallSupport(freeplay_api_key, api_base, **kwargs)
        self.provider_config = provider_config
        self.client_flavor = flavor
        self.freeplay_api_key = freeplay_api_key
        self.api_base = api_base

    def create_session(self, project_id: str, tag: str = default_tag) -> Session:
        project_session = self.call_support.create_session(project_id, tag)
        prompts = self.call_support.get_prompts(project_id, tag)
        return Session(self.call_support, project_session['session_id'], prompts, self.client_flavor,
                       self.provider_config, tag)

    def restore_session(
            self,
            project_id: str,
            session_id: str,
            template_name: str,
            variables: dict[str, str],
            tag: str = default_tag,
            flavor: Optional[Flavor] = None,
            **kwargs: Any
    ) -> CompletionResponse:
        prompts = self.call_support.get_prompts(project_id, tag)
        completion_flavor = flavor or self.client_flavor
        return self.call_support.prepare_and_make_call(
            session_id=session_id,
            prompts=prompts,
            template_name=template_name,
            variables=variables,
            flavor=completion_flavor,
            provider_config=self.provider_config,
            tag=tag,
            completion_parameters=LLMParameters(kwargs),
        )

    def get_completion(
            self,
            project_id: str,
            template_name: str,
            variables: dict[str, str],
            tag: str = default_tag,
            flavor: Optional[Flavor] = None,
            **kwargs: Any
    ) -> CompletionResponse:
        project_session = self.call_support.create_session(project_id, tag)
        prompts = self.call_support.get_prompts(project_id, tag)
        completion_flavor = flavor or self.client_flavor

        return self.call_support.prepare_and_make_call(project_session['session_id'],
                                                       prompts,
                                                       template_name,
                                                       variables,
                                                       completion_flavor,
                                                       self.provider_config,
                                                       tag,
                                                       completion_parameters=LLMParameters(kwargs))

    def get_completion_stream(
            self,
            project_id: str,
            template_name: str,
            variables: dict[str, str],
            tag: str = default_tag,
            flavor: Optional[Flavor] = None,
            **kwargs: Any
    ) -> Generator[CompletionChunk, None, None]:
        project_session = self.call_support.create_session(project_id, tag)
        prompts = self.call_support.get_prompts(project_id, tag)
        completion_flavor = flavor or self.client_flavor

        return self.call_support.prepare_and_make_call_stream(project_session['session_id'],
                                                              prompts,
                                                              template_name,
                                                              variables,
                                                              completion_flavor,
                                                              self.provider_config,
                                                              tag,
                                                              completion_parameters=LLMParameters(kwargs))

    def create_test_run(self, project_id: str, testlist: str) -> FreeplayTestRun:
        response = api_support.post_raw(
            api_key=self.freeplay_api_key,
            url=f'{self.api_base}/projects/{project_id}/test-runs',
            payload={'playlist_name': testlist},
        )

        json_dom = response.json()

        return FreeplayTestRun(
            self.call_support,
            self.client_flavor,
            self.provider_config,
            json_dom['test_run_id'],
            json_dom['inputs'])

    def start_chat(
            self,
            project_id: str,
            template_name: str,
            variables: Variables,
            tag: str = default_tag,
            **kwargs: Any
    ) -> Tuple[ChatSession, ChatCompletionResponse]:
        session = self.__create_chat_session(project_id, tag, template_name, variables)
        completion_response = session.start_chat(**kwargs)
        return session, completion_response

    def restore_chat_session(
            self,
            project_id: str,
            template_name: str,
            session_id: str,
            variables: Variables,
            tag: str = default_tag,
            messages: Optional[list[ChatMessage]] = None,
            flavor: Optional[ChatFlavor] = None) -> ChatSession:
        prompts = self.call_support.get_prompts(project_id, tag)
        chat_flavor = flavor or require_chat_flavor(self.client_flavor) if self.client_flavor else None
        return ChatSession(
            call_support=self.call_support,
            session_id=session_id,
            prompts=prompts,
            flavor=chat_flavor,
            provider_config=self.provider_config,
            template_name=template_name,
            variables=variables,
            tag=tag,
            messages=messages or []
        )

    def start_chat_stream(
            self,
            project_id: str,
            template_name: str,
            variables: Variables,
            tag: str = default_tag,
            **kwargs: Any
    ) -> Tuple[ChatSession, Generator[CompletionChunk, None, None]]:
        """Returns a chat session, the base prompt template messages, and a streamed response from the LLM."""
        session = self.__create_chat_session(project_id, tag, template_name, variables)
        completion_response = session.start_chat_stream(**kwargs)
        return session, completion_response

    def __create_chat_session(self, project_id: str, tag: str, template_name: str, variables: Variables) -> ChatSession:
        chat_flavor = require_chat_flavor(self.client_flavor) if self.client_flavor else None

        project_session = self.call_support.create_session(project_id, tag)
        prompts = self.call_support.get_prompts(project_id, tag)
        return ChatSession(
            self.call_support,
            project_session['session_id'],
            prompts,
            chat_flavor,
            self.provider_config,
            template_name,
            variables,
            tag)


def pick_flavor_from_config(completion_flavor: Optional[Flavor], ui_flavor_name: Optional[str]) -> Flavor:
    ui_flavor = Flavor.get_by_name(ui_flavor_name) if ui_flavor_name else None
    flavor = completion_flavor or ui_flavor

    if flavor is None:
        raise FreeplayError(
            "Flavor must be configured on either the Freeplay client, completion call, or in the Freeplay UI. Unable to fulfill request.")

    return flavor


def get_chat_flavor_from_config(completion_flavor: Optional[Flavor], ui_flavor_name: Optional[str]) -> ChatFlavor:
    flavor = pick_flavor_from_config(completion_flavor, ui_flavor_name)
    return require_chat_flavor(flavor)


def require_chat_flavor(flavor: Flavor) -> ChatFlavor:
    if not isinstance(flavor, ChatFlavor):
        raise FreeplayError('A Chat flavor is required to start a chat session.')

    return flavor
