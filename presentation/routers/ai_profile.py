import typer

from pkg.controller import Controller


class AIProfileRouter:
    def __init__(
        self,
        create_controller: Controller,
        list_controller: Controller,
        update_controller: Controller,
        delete_controller: Controller,
        use_controller: Controller,
    ):
        self.create_controller = create_controller
        self.list_controller = list_controller
        self.update_controller = update_controller
        self.delete_controller = delete_controller
        self.use_controller = use_controller

    def __call__(self) -> typer.Typer:
        self.router = typer.Typer(name="aiprofile", help="Manage AI Profiles.")
        self.router.command("create")(self.create_controller)
        self.router.command("list")(self.list_controller)
        self.router.command("update")(self.update_controller)
        self.router.command("delete")(self.delete_controller)
        self.router.command("use")(self.use_controller)
        return self.router
