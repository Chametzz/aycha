from collections.abc import Callable

import questionary

from domain.dtos.create_ai_profile_params import CreateAIProfileParams
from domain.enums.ai_provider import AIProvider


def prompt_create_ai_profile(
    exists_by_id: Callable[[str], bool],
) -> CreateAIProfileParams:
    provider: AIProvider | None = questionary.select(
        "Select AI Provider:",
        choices=[questionary.Choice(title=p.display_name, value=p) for p in AIProvider],
    ).ask()

    if provider is None:
        raise KeyboardInterrupt()

    model_version: str = questionary.text(
        "Enter Model Version:",
        validate=_validate_not_empty,
    ).ask()

    if model_version is None:
        raise KeyboardInterrupt()

    base_id = (
        f"{provider.value}-{model_version}".lower().replace(":", "-").replace("/", "-")
    )
    default_id = base_id
    counter = 1
    while exists_by_id(default_id):
        default_id = f"{base_id}-{counter}"

    id: str = questionary.text(
        "Enter a unique AI Profile ID:",
        default=default_id,
        validate=_validate_not_empty,
    ).ask()

    if id is None:
        raise KeyboardInterrupt()

    api_key = None
    if provider.requires_api_key:
        api_key: str = questionary.text(
            "API Key:",
            validate=_validate_not_empty,
        ).ask()

        if api_key is None:
            raise KeyboardInterrupt()

    base_url: str = questionary.text(
        "Base URL (optional, press Enter to skip):",
        validate=lambda val: (
            True
            if not val.strip() or val.startswith(("http://", "https://"))
            else "URL must start with 'http://' or 'https://'"
        ),
    ).ask()

    if base_url is None:
        raise KeyboardInterrupt()

    return CreateAIProfileParams(
        id=id.strip(),
        provider=provider,
        model_version=model_version.strip(),
        api_key=api_key.strip() if api_key else None,
        base_url=base_url.strip(),
    )


def _validate_not_empty(val: str) -> bool | str:
    if not val.strip():
        return "This field cannot be empty."
    return True


def _validate_id(val: str, exists_by_id: Callable[[str], bool]):
    clean_val = val.strip()
    if not clean_val:
        return "This field cannot be empty"
    if exists_by_id(clean_val):
        return f"AI Profile ID '{clean_val}' already exists. Please choose another one."
    return True
