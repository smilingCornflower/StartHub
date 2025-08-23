from enum import StrEnum


class RoleEnum(StrEnum):
    USER = "user"
    BLOGGER = "blogger"

    ADMIN = "admin"
    MODERATOR = "moderator"
    SUPER_ADMIN = "super_admin"

    @classmethod
    def get_default(cls) -> str:
        return cls.USER
