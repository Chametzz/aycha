import json
from pathlib import Path
from typing import Any

from typer import get_app_dir

from domain.constants import APP_NAME
from domain.entities.ai_profile import AIProfile
from domain.enums.ai_provider import AIProvider
from domain.repositories.ai_profile_repository import AIProfileRepository

DEFAULT_DATA: dict[str, Any] = {"active_id": None, "ai_profiles": {}}


class AIProfileRepositoryImpl(AIProfileRepository):
    def __init__(self):
        app_dir = Path(get_app_dir(APP_NAME))
        app_dir.mkdir(parents=True, exist_ok=True)
        self.file_path = app_dir / "ai_profiles.json"

    def _ensure_file_exists(self) -> None:
        if not self.file_path.exists():
            self._save_json(DEFAULT_DATA)

    def _load_file(self) -> dict[str, Any]:
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return DEFAULT_DATA.copy()

    def _save_file(self, data: dict[str, Any]) -> None:
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def _dict_to_entity(self, id: str, item: dict[str, Any]) -> AIProfile:
        return AIProfile(
            id=id,
            provider=AIProvider(item["provider"]),
            model_version=item["model_version"],
            api_key=item.get("api_key"),
            base_url=item.get("base_url"),
        )

    def _entity_to_dict(self, ai_profile: AIProfile) -> dict[str, Any]:
        return {
            "provider": ai_profile.provider.value,
            "model_version": ai_profile.model_version,
            "api_key": ai_profile.api_key,
            "base_url": ai_profile.base_url,
        }

    def save(self, ai_profile: AIProfile) -> None:
        data = self._load_file()
        data["ai_profiles"][ai_profile.id] = self._entity_to_dict(ai_profile)
        self._save_file(data)

    def get(self) -> list[AIProfile]:
        data = self._load_file()
        return [
            self._dict_to_entity(id, item) for id, item in data["ai_profiles"].items()
        ]

    def get_by_id(self, id: str) -> AIProfile | None:
        data = self._load_file()
        item = data["ai_profiles"].get(id)
        if not item:
            return None
        return self._dict_to_entity(id, item)

    def exists_by_id(self, id: str) -> bool:
        data = self._load_file()
        return id in data["ai_profiles"]

    def get_active(self) -> AIProfile | None:
        data = self._load_file()
        active_id = data.get("active_id")
        if not active_id:
            return None
        return self.get_by_id(active_id)

    def update_id(self, old_id: str, new_id: str) -> None:
        data = self._load_file()
        ai_profiles = data["ai_profiles"]

        if old_id in ai_profiles:
            ai_profiles[new_id] = ai_profiles.pop(old_id)
            if data.get("active_id") == old_id:
                data["active_id"] = new_id
            self._save_file(data)

    def set_active(self, id: str) -> None:
        data = self._load_file()
        if id in data["ai_profiles"]:
            data["active_id"] = id
            self._save_file(data)

    def delete(self, id: str) -> None:
        data = self._load_file()
        if id in data["ai_profiles"]:
            del data["ai_profiles"][id]
            if data.get("active_id") == id:
                data["active_id"] = None
            self._save_file(data)
