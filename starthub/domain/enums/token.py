from enum import StrEnum


class TokenTypeEnum(StrEnum):
    ACCESS = "access"
    REFRESH = "refresh"


class TokenNameEnum(StrEnum):
    ACCESS_TOKEN = "access_token"
    REFRESH_TOKEN = "refresh_token"
