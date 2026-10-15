import typer

from pkg.controller import Controller


class SystemPromptRouter:
    def __init__(self, update_controller: Controller):
        self.update_controller = update_controller

    def __call__(self) -> typer.Typer:
        self.router = typer.Typer(name="system-prompt", help="Manage system prompts")
        self.router.command("update")(self.update_controller)
