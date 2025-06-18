from enum import StrEnum


class RoleEnum(StrEnum):
    USER = "user"
    BLOGGER = "blogger"

    @classmethod
    def get_default(cls) -> str:
        return cls.USER
