from abc import ABC, abstractmethod

from domain.entities.ai_profile import AIProfile


class AIService(ABC):
    def __init__(self, ai_profile: AIProfile):
        self.ai_profile = ai_profile

    @abstractmethod
    def generate_response(self, prompt: str, system_prompt: str | None = None) -> str:
        pass
