from domain.entities.ai_profile import AIProfile
from domain.repositories.ai_profile_repository import AIProfileRepository


class GetAIProfilesUseCase:
    def __init__(self, repository: AIProfileRepository):
        self.repository = repository

    def __call__(self) -> list[AIProfile]:
        return self.repository.get()
