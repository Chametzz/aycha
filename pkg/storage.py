from pathlib import Path

import typer

from domain.constants import APP_NAME


def get_app_dir() -> Path:
    app_dir = Path(typer.get_app_dir(APP_NAME))
    app_dir.mkdir(parents=True, exist_ok=True)
    return app_dir
