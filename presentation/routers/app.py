import typer


class AppRouter:
    def __init__(self, *args):
        self.routers = args

    def __call__(self) -> typer.Typer:
        app = typer.Typer(
            name="chai", help="Manage AI profiles to generate git commits."
        )
        for r in self.routers:
            app.add_typer(r)
        return app
