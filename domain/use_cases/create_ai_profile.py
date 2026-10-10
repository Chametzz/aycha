from domain.dtos.create_ai_profile_params import CreateAIProfileParams
from domain.entities.ai_profile import AIProfile
from domain.repositories.ai_profile_repository import AIProfileRepository


class CreateAIProfileUseCase:
    def __init__(self, repository: AIProfileRepository):
        self.repository = repository

    def __call__(self, params: CreateAIProfileParams) -> AIProfile:
        if self.repository.exists_by_id(params.id):
            raise ValueError("This AI Profile already exists.")
        new_ai_profile = AIProfile(
            id=params.id,
            provider=params.provider,
            model_version=params.model_version,
            api_key=params.api_key,
            base_url=params.base_url,
        )
        self.repository.save(new_ai_profile)
        return new_ai_profile
