from abc import ABC, abstractmethod

from domain.enums.system_prompt_registry import SystemPromptRegistry


class SystemPromptService(ABC):
    @abstractmethod
    def save(self, key: SystemPromptRegistry, content: str) -> None:
        pass

    @abstractmethod
    def get(self, key: SystemPromptRegistry) -> str:
        pass
