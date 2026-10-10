import questionary

from domain.entities.ai_profile import AIProfile


def prompt_select_ai_profile(ai_profiles: list[AIProfile]) -> AIProfile:
    selected: AIProfile = questionary.select(
        "Select an AI Profile:",
        choices=[questionary.Choice(title=ai_p.id, value=ai_p) for ai_p in ai_profiles],
    ).ask()

    return selected
