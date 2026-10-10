from abc import ABC, abstractmethod

from domain.entities.ai_profile import AIProfile


class AIProfileRepository(ABC):
    @abstractmethod
    def save(self, ai_profile: AIProfile) -> None:
        pass

    @abstractmethod
    def get(self) -> list[AIProfile]:
        pass

    @abstractmethod
    def exists_by_id(self, id: str) -> bool:
        pass

    @abstractmethod
    def get_by_id(self, id: str) -> AIProfile | None:
        pass

    @abstractmethod
    def get_active(self) -> AIProfile | None:
        pass

    @abstractmethod
    def set_active(self, id: str) -> None:
        pass

    @abstractmethod
    def update_id(self, old_id: str, new_id: str) -> None:
        pass

    @abstractmethod
    def delete(self, id: str) -> None:
        pass
