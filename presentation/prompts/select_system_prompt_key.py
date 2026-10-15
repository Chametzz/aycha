import questionary

from domain.enums.system_prompt_key import SystemPromptKey


def prompt_select_system_prompt_key(
    system_prompts: list[SystemPromptKey],
) -> SystemPromptKey:
    selected: SystemPromptKey = questionary.select(
        "Select a system prompt:",
        choices=[
            questionary.Choice(title=s_p.display_name, value=s_p)
            for s_p in system_prompts
        ],
    ).ask()

    return selected
