from domain.repositories.ai_profile_repository import AIProfileRepository


class DeleteAIProfileUseCase:
    def __init__(self, repository: AIProfileRepository):
        self.repository = repository

    def __call__(self, id: str) -> None:
        self.repository.delete(id)
