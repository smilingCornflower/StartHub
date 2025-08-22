from enum import StrEnum


class RoleEnum(StrEnum):
    USER = "user"
    BLOGGER = "blogger"
    ADMIN = "admin"

    @classmethod
    def get_default(cls) -> str:
        return cls.USER
