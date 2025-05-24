from dataclasses import dataclass


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
class AccessPayloadDto:
    sub: str
    email: str
    iat: int
    exp: int
    type: str
