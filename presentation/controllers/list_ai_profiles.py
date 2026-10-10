import typer

from domain.repositories.ai_profile_repository import AIProfileRepository
from pkg.controller import Controller


class ListAIProfilesController(Controller):
    def __init__(
        self,
        repository: AIProfileRepository,
    ):
        self.repository = repository

    def __call__(self) -> None:
        try:
            ai_profiles = self.repository.get()
            active_profile = self.repository.get_active()
            active_id = active_profile.id if active_profile else None
        except ValueError as err:
            typer.secho(f"Error: {err}", fg=typer.colors.RED, bold=True)
            raise typer.Exit(code=1)

        if not ai_profiles:
            typer.echo("No AI Profiles found.")
            return

        typer.secho("\nRegistered AI Profiles:", fg=typer.colors.CYAN, bold=True)
        for ai_profile in ai_profiles:
            is_active = ai_profile.id == active_id
            active_indicator = " (Active)" if is_active else ""

            api_key_display = "••••" if ai_profile.api_key else "Not set"
            base_url_display = ai_profile.base_url or "Not set"
            ai_profile_line = (
                f"- [{ai_profile.id}]{active_indicator} {ai_profile.provider.display_name} | "
                f"Model: {ai_profile.model_version} | "
                f"API Key: {api_key_display} | "
                f"Base URL: {base_url_display}"
            )

            if is_active:
                typer.secho(ai_profile_line, fg=typer.colors.GREEN, bold=True)
            else:
                typer.echo(ai_profile_line)
