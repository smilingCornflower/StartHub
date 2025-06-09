from dataclasses import dataclass

from domain.enums.token import TokenTypeEnum


@dataclass(frozen=True)
class AccessTokenVo:
    value: str


@dataclass(frozen=True)
class RefreshTokenVo:
    value: str


@dataclass(frozen=True)
class TokenPairVo:
    access: AccessTokenVo
    refresh: RefreshTokenVo


@dataclass(frozen=True)
class AccessPayload:
    sub: str
    email: str
    iat: int
    exp: int
    type: str = TokenTypeEnum.ACCESS

    def __post_init__(self) -> None:
        """:raises ValueError:"""
        if self.type != TokenTypeEnum.ACCESS:
            raise ValueError("Token type must be access.")


@dataclass(frozen=True)
class RefreshPayload:
    sub: str
    iat: int
    exp: int
    type: str = TokenTypeEnum.REFRESH

    def __post_init__(self) -> None:
        """:raises ValueError:"""
        if self.type != TokenTypeEnum.REFRESH:
            raise ValueError("Token type must be refresh.")
