import questionary

from domain.enums.system_prompt_registry import SystemPromptRegistry


def prompt_select_system_prompt(
    system_prompts: list[SystemPromptRegistry],
) -> SystemPromptRegistry:
    selected: SystemPromptRegistry = questionary.select(
        "Select a system prompt:",
        choices=[
            questionary.Choice(title=s_p.display_name, value=s_p)
            for s_p in system_prompts
        ],
    ).ask()

    return selected
