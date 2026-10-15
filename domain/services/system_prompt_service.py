from abc import ABC, abstractmethod

from domain.enums.system_prompt_key import SystemPromptKey


class SystemPromptService(ABC):
    @abstractmethod
    def save(self, key: SystemPromptKey, content: str) -> None:
        pass

    @abstractmethod
    def get(self, key: SystemPromptKey) -> str | None:
        pass

    @abstractmethod
    def get_or_default(self, key: SystemPromptKey) -> str:
        pass
