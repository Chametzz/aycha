from dataclasses import dataclass

from domain.enums.ai_provider import AIProvider


@dataclass(frozen=True)
class UpdateAIProfileParams:
    new_id: str | None
    provider: AIProvider
    model_version: str
    api_key: str | None
    base_url: str | None
