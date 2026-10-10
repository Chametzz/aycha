from typing import Annotated

import typer

from domain.use_cases.generate_commit_message import (
    GenerateCommitMessageUseCase,
)
from pkg.controller import Controller


class GitCommitController(Controller):
    def __init__(self, generate_commit_messsage_use_case: GenerateCommitMessageUseCase):
        self.generate_commit_message_use_case = generate_commit_messsage_use_case

    def __call__(
        self,
        context: Annotated[
            str | None,
            typer.Option(
                "--message",
                "-m",
                help="Additional context or hint to guide the AI commit message generation.",
            ),
        ] = None,
    ):
        typer.echo("Generating commit message with AI...")

        try:
            commit_message = self.generate_commit_message_use_case(context)
        except ValueError as err:
            typer.secho(f"Error: {err}", fg=typer.colors.RED, bold=True)
            raise typer.Exit(code=1)

        typer.secho("\nGenerated Commit Message:", fg=typer.colors.CYAN, bold=True)
        typer.echo(commit_message)
