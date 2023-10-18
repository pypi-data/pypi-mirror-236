import copy
import logging
from dataclasses import dataclass
from typing import Any, Optional

logger = logging.getLogger(__name__)


@dataclass
class LLMParameters(dict[str, Any]):
    def __init__(self, members: dict[str, Any]) -> None:
        super().__init__(members)

    @classmethod
    def empty(cls) -> 'LLMParameters':
        return LLMParameters({})

    def merge_and_override(self, additional_params: Optional['LLMParameters']) -> 'LLMParameters':
        updated_params = copy.deepcopy(self)

        if additional_params is not None:
            for model_param_key, value in additional_params.items():
                logger.debug(f"Overriding parameter '{model_param_key}' using value '{value}' from get_completion call")
                updated_params[model_param_key] = value

        return updated_params

    def pop(self, key: str, default: Optional[Any] = None) -> Any:
        return super().pop(key, default)
