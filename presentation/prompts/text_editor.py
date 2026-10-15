import tempfile
from pathlib import Path

import click


def prompt_text_editor(initial_text: str = "") -> str:
    with tempfile.NamedTemporaryFile(
        mode="w+", suffix=".txt", delete=False, encoding="utf-8"
    ) as temp:
        temp.write(initial_text)
        temp_path = temp.name
    try:
        click.edit(filename=temp_path)

        text = Path(temp_path).read_text(encoding="utf-8")
        return text.strip()
    finally:
        Path(temp_path).unlink(missing_ok=True)
