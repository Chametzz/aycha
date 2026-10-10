from google import genai

from domain.entities.ai_profile import AIProfile
from domain.services.ai_service import AIService


class GeminiAIService(AIService):
    def __init__(self, ai_profile: AIProfile):
        super().__init__(ai_profile)
        self.client = genai.Client(api_key=self.ai_profile.api_key)

    def generate_response(self, prompt: str, system_prompt: str | None = None) -> str:
        config = {}
        if system_prompt:
            config["system_instruction"] = system_prompt
        response = self.client.models.generate_content(
            model=self.ai_profile.model_version,
            contents=prompt,
            config=config if config else None,
        )

        return response.text.strip()
