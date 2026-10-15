import json
from pathlib import Path
from typing import Any

from typer import get_app_dir

from domain.constants import APP_NAME
from domain.enums.system_prompt_key import SystemPromptKey
from domain.services.system_prompt_service import SystemPromptService

DEFAULT_DATA: dict[str, Any] = {}


class SystemPromptServiceImpl(SystemPromptService):
    def __init__(self):
        app_dir = Path(get_app_dir(APP_NAME))
        app_dir.mkdir(parents=True, exist_ok=True)
        self.file_path = app_dir / "system_prompts.json"

    def _ensure_file_exists(self) -> None:
        if not self.file_patht.exists():
            self._save_file(DEFAULT_DATA)

    def _load_file(self) -> dict[str, Any]:
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return DEFAULT_DATA.copy()

    def _save_file(self, data: dict[str, Any]) -> None:
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def save(self, key: SystemPromptKey, content: str) -> None:
        data = self._load_file()
        data[key.value] = content
        self._save_file(data)

    def get(self, key: SystemPromptKey) -> str | None:
        data = self._load_file()
        content = data.get(key.value)

        if content is not None:
            cleaned_content = content.strip()
            if cleaned_content:
                return cleaned_content

        return ""

    def get_or_default(self, key: SystemPromptKey):
        if system_prompt := self.get(key):
            return system_prompt
        match key:
            case SystemPromptKey.GIT_COMMIT:
                return (
                    "You are an expert developer assistant. "
                    "Generate a standard-compliant conventional commit message based on the provided diff. "
                    "CRITICAL: Output ONLY the plain text commit message. "
                    "Do NOT use markdown code blocks (no ```, no ```text, no backticks at all)."
                )
            case _:
                raise ValueError(f"System Prompt not supported: {key}")
