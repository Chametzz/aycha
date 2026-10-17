import json
from abc import ABC, abstractmethod
from typing import Any

from pkg.storage import get_app_dir


class Migration(ABC):
    @property
    @abstractmethod
    def version(self) -> str:
        pass

    def __call__(self):
        pass

    @classmethod
    def execute(cls, file_name: str, current_version: str, migrations: list[Migration]):
        app_dir = get_app_dir()
        save_file = app_dir / file_name

        try:
            with open(save_file, "r", encoding="utf-8") as f:
                save_dict: dict[str, Any] = json.load(f)
        except json.JSONDecodeError, FileNotFoundError:
            save_dict = {}

        old_version = save_dict.get("version")

        if old_version == current_version:
            return

        pending_migs = migrations[
            next(
                (i + 1 for i, m in enumerate(migrations) if m.version == old_version), 0
            ) :
        ]

        for mig in pending_migs:
            mig()
            save_dict["version"] = mig.version
            with open(save_file, "w", encoding="utf-8") as f:
                json.dump(save_dict, f, indent=2)
            if mig.version == current_version:
                break
