from enum import Enum


class SystemPromptRegistry(Enum):
    GIT_COMMIT = (
        "git_commit",
        "Git commit",
    )

    def __init__(self, key: str, display_name: str):
        self._value_ = key
        self.display_name = display_name

    @classmethod
    def _missing_(cls, value):
        for member in cls:
            if member.value == value:
                return member
        return super()._missing_(value)
