from enum import Enum


class AIProvider(Enum):
    GROQ = ("groq", "Groq", True)
    GEMINI = ("gemini", "Google Gemini", True)

    def __init__(self, value: str, display_name: str, requires_api_key: bool):
        self._value_ = value
        self.display_name = display_name
        self.requires_api_key = requires_api_key

    @classmethod
    def _missing_(cls, value):
        for member in cls:
            if member.value == value:
                return member
        return super()._missing_(value)
