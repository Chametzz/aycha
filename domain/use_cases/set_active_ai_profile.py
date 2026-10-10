from domain.repositories.ai_profile_repository import AIProfileRepository


class SetActiveAIProfileUseCase:
    def __init__(self, repository: AIProfileRepository):
        self.repository = repository

    def __call__(self, id: str) -> None:
        ai_profile = self.repository.get_by_id(id)
        if not ai_profile:
            raise ValueError(f"AI Profile with ID {id} not found")
        self.repository.set_active(id)
