from typing import Annotated

import typer

from domain.enums.system_prompt_key import SystemPromptKey
from domain.services.system_prompt_service import SystemPromptService
from pkg.controller import Controller
from presentation.prompts.select_system_prompt_key import (
    prompt_select_system_prompt_key,
)
from presentation.prompts.text_editor import prompt_text_editor


class UpdateSystemPromptKeyController(Controller):
    def __init__(self, service: SystemPromptService):
        self.service = service

    def __call__(
        self,
        key: Annotated[
            str | None,
            typer.Option(
                "--key",
                "-k",
                help="Key of the system prompt to update",
            ),
        ] = None,
    ):
        try:
            if key:
                registry = SystemPromptKey(key)
            else:
                registry = prompt_select_system_prompt_key(SystemPromptKey)
        except ValueError:
            typer.secho(f"Error: '{key}' is not valid system prompt key.")
        current_content = self.service.get(registry)
        new_content = prompt_text_editor(current_content)

        if new_content is None:
            typer.secho(
                "Update cancelled: no content provided.", fg=typer.colors.YELLOW
            )
            return

        if new_content == current_content:
            typer.secho(
                "No changes made: the prompt content is identical.",
                fg=typer.colors.BLUE,
            )
            return

        self.service.save(registry, new_content)
        typer.secho(
            f"{registry.display_name} system prompt updated successfully!",
            fg=typer.colors.GREEN,
        )
