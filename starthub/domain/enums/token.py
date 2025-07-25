from enum import StrEnum


class TokenTypeEnum(StrEnum):
    ACCESS = "access"
    REFRESH = "refresh"
    ANONYMOUS = "anonymous"


class TokenNameEnum(StrEnum):
    ACCESS_TOKEN = "access_token"
    REFRESH_TOKEN = "refresh_token"
    ANONYMOUS_TOKEN = "anonymous_token"
