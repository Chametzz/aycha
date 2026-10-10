from abc import abstractmethod

from domain.entities.ai_profile import AIProfile
from domain.services.ai_service import AIService


class AIServiceProvider:
    @abstractmethod
    def get(self, ai_profile: AIProfile) -> AIService:
        pass
