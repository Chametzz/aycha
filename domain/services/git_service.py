from abc import ABC, abstractmethod


class GitService(ABC):
    @abstractmethod
    def get_staged_diff(self) -> str:
        pass

    @abstractmethod
    def execute_commit(self, message: str):
        pass
