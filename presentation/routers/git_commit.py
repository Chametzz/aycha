import typer

from pkg.controller import Controller


class GitCommitRouter:
    def __init__(self, controller: Controller):
        self.controller = controller

    def __call__(self) -> typer.Typer:
        self.router = typer.Typer(
            name="commit",
            help="Generate a semantic commit message based on staged changes and an optional hint.",
        )
        self.router.callback(invoke_without_command=True)(self.controller)
        return self.router
