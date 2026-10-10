from typing import Annotated

import typer

from domain.repositories.ai_profile_repository import AIProfileRepository
from domain.use_cases.delete_ai_profile import DeleteAIProfileUseCase
from pkg.controller import Controller
from presentation.prompts.delete_ai_profile import prompt_delete_ai_profile
from presentation.prompts.select_ai_profile import prompt_select_ai_profile


class DeleteAIProfileController(Controller):
    def __init__(
        self,
        repository: AIProfileRepository,
        delete_ai_profile_use_case: DeleteAIProfileUseCase,
    ):
        self.repository = repository
        self.delete_ai_profile_use_case = delete_ai_profile_use_case

    def __call__(
        self,
        id: Annotated[
            str | None,
            typer.Option("--id", "-i", help="ID of the AI Profile to delete."),
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
                typer.echo("No AI profiles available to delete.")
                return

            target_ai_profile = prompt_select_ai_profile(ai_profiles)
            if target_ai_profile is None:
                return
        try:
            is_confirmed = prompt_delete_ai_profile(target_ai_profile)
        except KeyboardInterrupt:
            typer.echo("\nDeletion cancelled.")
            return

        if not is_confirmed:
            typer.echo("Deletion cancelled.")
            return

        try:
            self.delete_ai_profile_use_case(target_ai_profile.id)
        except ValueError as err:
            typer.secho(f"Error: {err}", fg=typer.colors.RED, bold=True)
            raise typer.Exit(code=1)

        typer.secho(
            f"AI Profile '{target_ai_profile.id}' deleted successfully!",
            fg=typer.colors.GREEN,
            bold=True,
        )
