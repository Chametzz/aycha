from dataclasses import dataclass

from domain.enums.ai_provider import AIProvider


@dataclass
class AIProfile:
    id: str
    provider: AIProvider
    model_version: str
    api_key: str | None = None
    base_url: str | None = None
