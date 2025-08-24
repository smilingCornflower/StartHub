from dataclasses import dataclass, field

from domain.enums.token import TokenTypeEnum


@dataclass(frozen=True)
class TokenPairDto:
    access_token: str
    refresh_token: str


@dataclass(frozen=True)
class AccessTokenDto:
    access_token: str


@dataclass(frozen=True)
class RefreshTokenDto:
    refresh_token: str


@dataclass(frozen=True)
class AnonymousTokenDto:
    anonymous_token: str


@dataclass(frozen=True)
class PayloadDto:
    type: str


@dataclass(frozen=True)
class AccessPayloadDto(PayloadDto):
    sub: str
    roles: list[str]
    email: str
    first_name: str
    last_name: str
    iat: int
    exp: int
    type: str = field(default=TokenTypeEnum.ACCESS, init=False)


@dataclass(frozen=True)
class AnonymousPayloadDto(PayloadDto):
    sub: str
    iat: int
    exp: int
    type: str = field(default=TokenTypeEnum.ANONYMOUS, init=False)
