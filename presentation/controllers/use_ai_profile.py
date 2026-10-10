from typing import Annotated

import typer

from domain.repositories.ai_profile_repository import AIProfileRepository
from domain.use_cases.set_active_ai_profile import SetActiveAIProfileUseCase
from pkg.controller import Controller
from presentation.prompts.select_ai_profile import prompt_select_ai_profile


class UseAIProfileController(Controller):
    def __init__(
        self,
        repository: AIProfileRepository,
        set_active_ai_profile_use_case: SetActiveAIProfileUseCase,
    ):
        self.repository = repository
        self.set_active_ai_profile_use_case = set_active_ai_profile_use_case

    def __call__(
        self,
        id: Annotated[
            str | None,
            typer.Option("--id", "-i", help="ID of the AI Profile to use."),
        ] = None,
    ) -> None:
        if id:
            target_ai_profile = self.repository.get_by_id(id)
            if target_ai_profile is None:
                typer.secho(
                    f"Error: AI Profile '{id}' not found.",
                    fg=typer.colors.RED,
                    bold=True,
                )
                raise typer.Exit(code=1)
        else:
            ai_profiles = self.repository.get()
            if not ai_profiles:
                typer.echo("No AI profiles available to select.")
                return

            try:
                target_ai_profile = prompt_select_ai_profile(ai_profiles)
            except KeyboardInterrupt:
                typer.echo("\nSelection cancelled.")
                return

            if target_ai_profile is None:
                return

        try:
            self.set_active_ai_profile_use_case(target_ai_profile.id)
        except ValueError as err:
            typer.secho(f"Error: {err}", fg=typer.colors.RED, bold=True)
            raise typer.Exit(code=1)

        typer.secho(
            f"AI Profile '{target_ai_profile.id}' is now active!",
            fg=typer.colors.GREEN,
            bold=True,
        )
