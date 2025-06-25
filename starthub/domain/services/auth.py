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
from domain.exceptions.auth import InvalidCredentialsException, InvalidTokenException, TokenExpiredException
from domain.exceptions.user import EmailAlreadyExistsException, UserNotFoundException
from domain.models.user import User
from domain.ports.service import AbstractDomainService
from domain.repositories.user import UserReadRepository, UserWriteRepository
from domain.value_objects.auth import LoginCredentials
from domain.value_objects.common import Id
from domain.value_objects.filter import UserFilter
from domain.value_objects.token import AccessPayload, AccessTokenVo, RefreshPayload, RefreshTokenVo, TokenPairVo
from domain.value_objects.user import Email, UserCreatePayload
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


class AuthService(AbstractDomainService):
    def __init__(
        self,
        token_service: TokenService,
        user_read_repository: UserReadRepository,
        user_write_repository: UserWriteRepository,
    ):
        self._token_service = token_service
        self._user_read_repository = user_read_repository
        self._user_write_repository = user_write_repository

    def check_user_existence(self, email: Email) -> None:
        """:raises UserNotFoundException:"""

        self._user_read_repository.get_by_email(email=email)

    def login(self, credentials: LoginCredentials) -> TokenPairVo:
        """
        :raises InvalidCredentialsException:
        """
        user: User = self._authenticate_user(credentials=credentials)
        logger.info(f"User '{credentials.email}' is successfully authenticated.")
        self._user_write_repository.update_last_login(user)
        logger.debug("last_login updated")

        return TokenPairVo(
            access=self._token_service.generate_access(user=user),
            refresh=self._token_service.generate_refresh(user=user),
        )

    def reissue_access(self, refresh_token: RefreshTokenVo) -> AccessTokenVo:
        """
        :raises TokenExpiredException:
        :raises InvalidTokenException: If token verification fails
        """
        payload: RefreshPayload = self._token_service.verify_refresh(token=refresh_token)
        try:
            user: User = self._user_read_repository.get_by_id(Id(value=int(payload.sub)))
        except UserNotFoundException:
            logger.error(f"Failed to find a user with id: {payload.sub}.")
            raise InvalidTokenException("Invalid access token.")

        return self._token_service.generate_access(user=user)

    def reissue_refresh(self, refresh_token: RefreshTokenVo) -> RefreshTokenVo:
        """
        :raises TokenExpiredException:
        :raises InvalidTokenException: If token verification fails
        """
        payload: RefreshPayload = self._token_service.verify_refresh(token=refresh_token)
        try:
            user: User = self._user_read_repository.get_by_id(Id(value=int(payload.sub)))
        except UserNotFoundException:
            logger.error(f"Failed to find a user with id: {payload.sub}.")
            raise InvalidTokenException("Invalid refresh token.")

        return self._token_service.generate_refresh(user=user)

    def _authenticate_user(self, credentials: LoginCredentials) -> User:
        """
        :raises InvalidCredentialsException:
        """
        try:
            user: User = self._user_read_repository.get_by_email(credentials.email)
        except UserNotFoundException:
            logger.error(f"Failed to find a user with email '{credentials.email}'.")
            raise InvalidCredentialsException("Invalid email or password.")

        if not user.check_password(credentials.password.value):
            logger.error(f"Incorrect password for the user {user.email}")
            raise InvalidCredentialsException("Invalid email or password.")

        return user


class RegistrationService(AbstractDomainService):
    def __init__(
        self,
        read_repository: UserReadRepository,
        write_repository: UserWriteRepository,
    ):
        self.read_repository = read_repository
        self.write_repository = write_repository

    def register(self, data: UserCreatePayload) -> User:
        """
        :raises EmailAlreadyExistsException:
        """
        logger.warning(f"Starting to register a user '{data.email.value}'.")
        self._check_email_already_exists(data.email)

        user: User = self.write_repository.create(data)
        logger.info(f"User {user.email} is registered successfully.")

        return user

    def _check_email_already_exists(self, email: Email) -> None:
        """:raises EmailAlreadyExistsException:"""
        result: list[User] = self.read_repository.get_all(UserFilter(email=email))
        if result:
            logger.error(f"The email '{email.value}' already in use.")
            raise EmailAlreadyExistsException(email.value)
        logger.debug(f"The email '{email.value}' is free to use.")
