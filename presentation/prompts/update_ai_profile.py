from collections.abc import Callable

import questionary

from domain.dtos.update_ai_profile_params import UpdateAIProfileParams
from domain.entities.ai_profile import AIProfile
from domain.enums.ai_provider import AIProvider


def prompt_update_ai_profile(
    ai_profile: AIProfile, exists_by_id: Callable[[str], bool]
) -> UpdateAIProfileParams:
    new_id: str | None = None
    provider = ai_profile.provider
    model_version = ai_profile.model_version
    api_key = ai_profile.api_key
    base_url = ai_profile.base_url

    while True:
        choices: list[questionary.Choice] = [
            questionary.Choice(
                title=f"ID: {new_id if new_id else ai_profile.id}", value="id"
            ),
            questionary.Choice(
                title=f"AI Provider: {provider.display_name}",
                value="provider",
            ),
            questionary.Choice(
                title=f"Model version: {model_version}",
                value="model_version",
            ),
            questionary.Choice(
                title=f"API Key: {'••••' if api_key else 'Not set'}",
                value="api_key",
            ),
            questionary.Choice(
                title=f"Base URL: {base_url or 'Not set'}",
                value="base_url",
            ),
            questionary.Choice(
                title="Save",
                value="save",
            ),
        ]

        field_selected = questionary.select(
            "Select the field to update.",
            choices=choices,
        ).ask()

        if field_selected is None:
            raise KeyboardInterrupt()

        match field_selected:
            case "id":
                user_input: str | None = questionary.text(
                    "New AI Profile ID:",
                    default=new_id if new_id else ai_profile.id,
                    validate=lambda val: _validate_id(val, ai_profile.id, exists_by_id),
                ).ask()
                if user_input is not None:
                    clean_input = user_input.strip()

                    if not clean_input or clean_input == ai_profile.id:
                        new_id = None
                    else:
                        new_id = clean_input
            case "provider":
                user_input: AIProvider | None = questionary.select(
                    "Select new AI Provider:",
                    choices=[
                        questionary.Choice(title=p.display_name, value=p)
                        for p in AIProvider
                    ],
                    default=provider,
                ).ask()

                if user_input is not None:
                    provider = user_input
                    if not provider.requires_api_key:
                        api_key = None
            case "model_version":
                user_input: str | None = questionary.text(
                    "New Model Version:",
                    default=model_version,
                    validate=_validate_not_empty,
                ).ask()
                if user_input is not None and user_input.strip():
                    model_version = user_input.strip()
            case "api_key":
                if not provider.requires_api_key:
                    questionary.print(
                        f"Provider '{provider.display_name}' does not require an API Key.",
                        style="bold yellow",
                    )
                    continue
                user_input: str | None = questionary.password("New API Key:").ask()

                if user_input is not None:
                    clean_input = user_input.strip()
                    api_key = clean_input if clean_input else None
            case "base_url":
                user_input: str | None = questionary.text(
                    "New Base URL (optional, press Enter to clear):",
                    default=base_url or "",
                    validate=lambda val: (
                        True
                        if not val.strip() or val.startswith(("http://", "https://"))
                        else "URL must start with 'http://' or 'https://'"
                    ),
                ).ask()

                if user_input is not None:
                    clean_url = user_input.strip()
                    base_url = clean_url if clean_url else None
            case "save":
                return UpdateAIProfileParams(
                    new_id=new_id,
                    provider=provider,
                    model_version=model_version,
                    api_key=api_key,
                    base_url=base_url,
                )


def _validate_not_empty(val: str) -> bool | str:
    if not val.strip():
        return "This field cannot be empty."
    return True


def _validate_id(
    val: str, current_id: str, exists_by_id: Callable[[str], bool]
) -> bool | str:
    clean_val = val.strip()
    if not clean_val:
        return "This field cannot be empty."
    if clean_val != current_id and exists_by_id(clean_val):
        return f"AI Profile ID '{clean_val}' already exists. Please choose another one."
    return True
