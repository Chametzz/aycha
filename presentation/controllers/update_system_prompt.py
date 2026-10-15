from typing import Annotated

import typer

from domain.enums.system_prompt_registry import SystemPromptRegistry
from domain.services.system_prompt_service import SystemPromptService
from pkg.controller import Controller
from presentation.prompts.select_system_prompt import prompt_select_system_prompt
from presentation.prompts.text_editor import prompt_text_editor


class UpdateSystemPromptController(Controller):
    def __init__(self, service: SystemPromptService):
        self.service = service

    def __call__(
        self,
        key: Annotated[
            str | None,
            typer.Option(
                "--id",
                "-i",
                "--key",
                "-k",
                help="Identifier of the system prompt to update",
            ),
        ] = None,
    ):
        try:
            if key:
                registry = SystemPromptRegistry(key)
            else:
                registry = prompt_select_system_prompt(SystemPromptRegistry)
        except ValueError:
            typer.secho(f"Error: '{key}' is not valid system prompt identifier.")

        new_content = prompt_text_editor(self.service.get(registry))

        if new_content:
            self.service.save(registry, new_content)
            typer.secho(
                f"{registry.display_name} system prompt updated sucessfully!",
                fg=typer.colors.GREEN,
            )
        else:
            typer.echo("Update cancelled")
