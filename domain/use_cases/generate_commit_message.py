from domain.repositories.ai_profile_repository import AIProfileRepository
from domain.services.ai_service_provider import AIServiceProvider
from domain.services.git_service import GitService


class GenerateCommitMessageUseCase:
    def __init__(
        self,
        git_service: GitService,
        ai_profile_repository: AIProfileRepository,
        ai_service_provider: AIServiceProvider,
    ):
        self.git_service = git_service
        self.ai_profile_repository = ai_profile_repository
        self.ai_service_provider = ai_service_provider

    def __call__(self, context: str | None) -> str:
        ai_profile = self.ai_profile_repository.get_active()
        if not ai_profile:
            raise ValueError(
                "No active AI profile found. Please set an active profile using 'chai aiprofile use <id>' or create one with 'chai aiprofile create'."
            )

        ai_service = self.ai_service_provider.get(ai_profile)

        staged_diff = self.git_service.get_changes()
        if not staged_diff.strip():
            raise ValueError("No staged changes found.")

        system_prompt = (
            "You are an expert developer assistant."
            "standard-compilant conventional commit message based on the provided diff."
        )

        prompt = f"Diff:\n{staged_diff}"
        if context:
            prompt += f"\n\nContext/Hint: {context}"
        message = ai_service.generate_response(prompt, system_prompt)

        self.git_service.execute_commit(message)

        return message
