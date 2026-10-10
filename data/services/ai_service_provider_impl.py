from data.services.geimini_ai_service import GeminiAIService
from data.services.groq_ai_service import GroqAIService
from domain.entities.ai_profile import AIProfile
from domain.enums.ai_provider import AIProvider
from domain.services.ai_service import AIService
from domain.services.ai_service_provider import AIServiceProvider


class AIServiceProviderImpl(AIServiceProvider):
    def get(self, ai_profile: AIProfile) -> AIService:
        match ai_profile.provider:
            case AIProvider.GROQ:
                return GroqAIService(ai_profile)
            case AIProvider.GEMINI:
                return GeminiAIService(ai_profile)
            case _:
                raise ValueError(f"AI Provider not supported: {ai_profile.provider}")
