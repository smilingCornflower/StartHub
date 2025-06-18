from dataclasses import asdict
from datetime import UTC, datetime

import jwt
from domain.constants import (
    ACCESS_DECODE_OPTIONS,
    ACCESS_TOKEN_LIFETIME,
    JWT_ALGORITHM,
    REFRESH_DECODE_OPTIONS,
    REFRESH_TOKEN_LIFETIME,
)
from domain.exceptions.auth import InvalidTokenException, TokenExpiredException
from domain.models.user import User
from domain.ports.service import AbstractDomainService
from domain.value_objects.token import AccessPayload, AccessTokenVo, RefreshPayload, RefreshTokenVo
from loguru import logger


class TokenService(AbstractDomainService):
    def __init__(
        self,
        secret_key: str,
        access_token_lifetime: int = ACCESS_TOKEN_LIFETIME,
        refresh_token_lifetime: int = REFRESH_TOKEN_LIFETIME,
    ):
        self.__secret_key = secret_key
        self.access_token_lifetime = access_token_lifetime
        self.refresh_token_lifetime = refresh_token_lifetime

    def generate_access(self, user: User) -> AccessTokenVo:
        """Generate a new access token for a user."""
        issued_at = int(datetime.now(UTC).timestamp())
        expires_at = issued_at + self.access_token_lifetime

        payload = AccessPayload(sub=str(user.id), email=user.email, iat=issued_at, exp=expires_at)
        token = jwt.encode(asdict(payload), key=self.__secret_key, algorithm=JWT_ALGORITHM)
        return AccessTokenVo(value=token)

    def generate_refresh(self, user: User) -> RefreshTokenVo:
        """Generate a new refresh token for a user."""
        issued_at = int(datetime.now(UTC).timestamp())
        expires_at = issued_at + self.refresh_token_lifetime

        payload = RefreshPayload(sub=str(user.id), iat=issued_at, exp=expires_at)
        token: str = jwt.encode(asdict(payload), key=self.__secret_key, algorithm=JWT_ALGORITHM)
        return RefreshTokenVo(value=token)

    def _verify_access(self, token: AccessTokenVo) -> AccessPayload:
        """
        Verify access token and return its payload.

        :raises ExpiredSignatureError: If the token has expired.
        :raises PyJWTError: If the token is invalid for any other reason
                            (e.g., malformed, invalid signature, or missing required claims).
        :raises ValueError: If payload['type'] is not 'refresh'.
        """
        payload = jwt.decode(
            token.value,
            self.__secret_key,
            algorithms=[JWT_ALGORITHM],
            options=ACCESS_DECODE_OPTIONS,
        )

        return AccessPayload(
            sub=payload["sub"],
            email=payload["email"],
            iat=payload["iat"],
            exp=payload["exp"],
            type=payload["type"],
        )

    def _verify_refresh(self, token: RefreshTokenVo) -> RefreshPayload:
        """
        Verify refresh token and return its payload.

        :raises ExpiredSignatureError: If the token has expired.
        :raises PyJWTError: If the token is invalid for any other reason
                            (e.g., malformed, invalid signature, or missing required claims).
        :raises ValueError: If payload['type'] is not 'refresh'.
        """
        payload = jwt.decode(
            token.value,
            self.__secret_key,
            algorithms=[JWT_ALGORITHM],
            options=REFRESH_DECODE_OPTIONS,
        )

        return RefreshPayload(
            sub=payload["sub"],
            iat=payload["iat"],
            exp=payload["exp"],
            type=payload["type"],
        )

    def verify_access(self, token: AccessTokenVo) -> AccessPayload:
        """
        Verify access token and return its payload.

        :raises TokenExpiredException:
        :raises InvalidTokenException: If token verification fails.
        """
        try:
            return self._verify_access(token=token)
        except jwt.ExpiredSignatureError as e:
            logger.exception(e)
            raise TokenExpiredException("Access token has expired.")
        except (jwt.PyJWTError, ValueError):
            raise InvalidTokenException("Invalid access token.")

    def verify_refresh(self, token: RefreshTokenVo) -> RefreshPayload:
        """
        Verify refresh token and return its payload.
        :raises TokenExpiredException:
        :raises InvalidTokenException: If token verification fails.
        """
        try:
            return self._verify_refresh(token=token)
        except jwt.ExpiredSignatureError as e:
            logger.exception(e)
            raise TokenExpiredException("Refresh token has expired.")
        except (jwt.PyJWTError, ValueError):
            raise InvalidTokenException("Invalid refresh token.")
