from groq import Groq

from domain.entities.ai_profile import AIProfile
from domain.services.ai_service import AIService


class GroqAIService(AIService):
    def __init__(self, ai_profile: AIProfile):
        super().__init__(ai_profile)
        self.client = Groq(
            api_key=self.ai_profile.api_key, base_url=self.ai_profile.base_url or None
        )

    def generate_response(self, prompt: str, system_prompt: str | None = None) -> str:
        messages = []

        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        messages.append({"role": "user", "content": prompt})

        chat_completion = self.client.chat.completions.create(
            messages=messages,
            model=self.ai_profile.model_version,
        )
        return chat_completion.choices[0].message.content
