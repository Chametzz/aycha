from domain.dtos.update_ai_profile_params import UpdateAIProfileParams
from domain.entities.ai_profile import AIProfile
from domain.repositories.ai_profile_repository import AIProfileRepository


class UpdateAIProfileUseCase:
    def __init__(self, repository: AIProfileRepository):
        self.repository = repository

    def __call__(self, target_id: str, params: UpdateAIProfileParams) -> AIProfile:
        ai_profile = self.repository.get_by_id(target_id)
        if ai_profile is None:
            raise ValueError(f"AI Profile with ID '{target_id}' does not exist.")

        effective_id = target_id

        if params.new_id and params.new_id != target_id:
            if self.repository.exists_by_id(params.new_id):
                raise ValueError(f"AI Profile ID '{params.new_id}' is already taken.")

            self.repository.update_id(target_id, params.new_id)
            effective_id = params.new_id

        updated_ai_profile = AIProfile(
            id=effective_id,
            provider=params.provider,
            model_version=params.model_version,
            api_key=params.api_key,
            base_url=params.base_url,
        )

        self.repository.save(updated_ai_profile)
        return updated_ai_profile
