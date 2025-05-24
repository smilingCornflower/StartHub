from domain.exceptions.auth import InvalidCredentialsException, InvalidTokenException
from domain.exceptions.user import EmailAlreadyExistsException, UsernameAlreadyExistsException, UserNotFoundException
from domain.models.user import User
from domain.repositories.user import UserReadRepository, UserWriteRepository
from domain.services.token import TokenService
from domain.value_objects.auth import LoginCredentials
from domain.value_objects.common import Id
from domain.value_objects.filter import UserFilter
from domain.value_objects.payload import UserCreatePayload
from domain.value_objects.token import AccessTokenVo, RefreshPayload, RefreshTokenVo, TokenPairVo
from domain.value_objects.user import Email, Username
from loguru import logger


class AuthService:
    def __init__(self, token_service: TokenService, user_read_repository: UserReadRepository):
        self._token_service = token_service
        self._user_read_repository = user_read_repository

    def login(self, credentials: LoginCredentials) -> TokenPairVo:
        """
        :raises InvalidCredentialsException:
        """
        user: User = self._authenticate_user(credentials=credentials)
        logger.info(f"User '{credentials.email}' is successfully authenticated.")

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
            user: User = self._user_read_repository.get_by_id(Id(int(payload.sub)))
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
            user: User = self._user_read_repository.get_by_id(Id(int(payload.sub)))
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


class RegistrationService:
    def __init__(
        self,
        read_repository: UserReadRepository,
        write_repository: UserWriteRepository,
    ):
        self.read_repository = read_repository
        self.write_repository = write_repository

    def register(self, data: UserCreatePayload) -> User:
        """
        :raises UsernameAlreadyExistsException:
        :raises EmailAlreadyExistsException:
        """
        logger.warning(f"Starting to register a user '{data.email.value}'.")
        self._check_username_already_exists(data.username)
        self._check_email_already_exists(data.email)

        user: User = self.write_repository.create(data)
        logger.info(f"User {user.email} is registered successfully.")

        return user

    def _check_username_already_exists(self, username: Username) -> None:
        """:raises UsernameAlreadyExistsException:"""
        result: list[User] = self.read_repository.get_all(UserFilter(username=username))
        if result:
            logger.error(f"The username '{username.value}' already in use.")
            raise UsernameAlreadyExistsException(username.value)
        logger.debug(f"The username '{username.value}' is free to use.")

    def _check_email_already_exists(self, email: Email) -> None:
        """:raises EmailAlreadyExistsException:"""
        result: list[User] = self.read_repository.get_all(UserFilter(email=email))
        if result:
            logger.error(f"The email '{email.value}' already in use.")
            raise EmailAlreadyExistsException(email.value)
        logger.debug(f"The email '{email.value}' is free to use.")
