import typer

from domain.repositories.ai_profile_repository import AIProfileRepository
from domain.use_cases.create_ai_profile import CreateAIProfileUseCase
from pkg.controller import Controller
from presentation.prompts.create_ai_profile import prompt_create_ai_profile


class CreateAIProfileController(Controller):
    def __init__(
        self,
        repository: AIProfileRepository,
        create_ai_profile_use_case: CreateAIProfileUseCase,
    ):
        self.repository = repository
        self.create_ai_profile_use_case = create_ai_profile_use_case

    def __call__(self):
        try:
            params = prompt_create_ai_profile(self.repository.exists_by_id)
        except KeyboardInterrupt:
            typer.echo("\nCreation cancelled.")
            return

        if params is None:
            typer.echo("Creation cancelled")
            return
        try:
            created_ai_profile = self.create_ai_profile_use_case(params)
        except ValueError as err:
            typer.secho(f"Error: {err}", fg=typer.colors.RED, bold=True)
            raise typer.Exit(code=1)

        typer.secho(
            f"AI Profile '{created_ai_profile.id}' created successfully!",
            fg=typer.colors.GREEN,
            bold=True,
        )
