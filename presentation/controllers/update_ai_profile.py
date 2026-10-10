from typing import Annotated

import typer

from domain.repositories.ai_profile_repository import AIProfileRepository
from domain.use_cases.update_ai_profile import UpdateAIProfileUseCase
from pkg.controller import Controller
from presentation.prompts.select_ai_profile import prompt_select_ai_profile
from presentation.prompts.update_ai_profile import prompt_update_ai_profile


class UpdateAIProfileController(Controller):
    def __init__(
        self,
        repository: AIProfileRepository,
        update_ai_profile_use_case: UpdateAIProfileUseCase,
    ):
        self.repository = repository
        self.update_ai_profile_use_case = update_ai_profile_use_case

    def __call__(
        self,
        id: Annotated[
            str | None,
            typer.Option("--id", "-i", help="ID of the AI Profile to update."),
        ] = None,
    ):
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
                typer.echo("No AI profiles available to update.")
                return
            target_ai_profile = prompt_select_ai_profile(ai_profiles)
            if target_ai_profile is None:
                return
        try:
            update_params = prompt_update_ai_profile(
                target_ai_profile, self.repository.exists_by_id
            )
        except KeyboardInterrupt:
            typer.echo("\nUpdate cancelled")
            return

        updated_ai_profile = self.update_ai_profile_use_case(
            target_ai_profile.id, update_params
        )
        typer.secho(
            f"AI Profile '{updated_ai_profile.id}' updated successfully!",
            fg=typer.colors.GREEN,
        )
