from enum import StrEnum


class LangCodeEnum(StrEnum):
    """ISO-639-1 Language codes"""

    RUSSIAN = "ru"
    ENGLISH = "en"
    KAZAKH = "kk"

    @classmethod
    def get_default(cls) -> "LangCodeEnum":
        return cls.ENGLISH
