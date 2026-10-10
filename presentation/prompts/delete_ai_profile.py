import questionary

from domain.entities.ai_profile import AIProfile


def prompt_delete_ai_profile(ai_profile: AIProfile) -> bool:
    confirmed: bool | None = questionary.confirm(
        f"Are you sure you want to delete the AI Profile '{ai_profile.id}'?",
        default=False,
    ).ask()

    if confirmed is None:
        return False

    return confirmed
