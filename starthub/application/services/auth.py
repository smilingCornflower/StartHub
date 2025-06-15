from application.converters.request_converters.auth import (
    request_cookies_to_access_token,
    request_cookies_to_refresh_token,
    request_data_to_email,
    request_data_to_login_credentials,
    request_data_to_user_create_payload,
)
from application.converters.resposne_converters.auth import (
    access_payload_to_dto,
    access_token_to_dto,
    token_pair_to_dto,
)
from application.dto.auth import AccessPayloadDto, AccessTokenDto, TokenPairDto
from application.ports.service import AbstractAppService
from domain.models.user import User
from domain.services.auth import AuthService, RegistrationService
from domain.services.token import TokenService
from domain.value_objects.auth import LoginCredentials
from domain.value_objects.token import AccessPayload, AccessTokenVo, RefreshTokenVo, TokenPairVo
from domain.value_objects.user import Email, UserCreatePayload
from loguru import logger


class RegistrationAppService(AbstractAppService):
    def __init__(self, registration_service: RegistrationService):
        self._registration_service = registration_service

    def register(self, request_data: dict[str, str]) -> User:
        """
        :raises KeyError: Missing required fields.
        :raises EmptyStringException:
        :raises InvalidEmailException:
        :raises PasswordValidationException:
        :raises pydantic.ValidationError: If fields has incorrect types
        :raises EmailAlreadyExistsException:
        """
        user_data: UserCreatePayload = request_data_to_user_create_payload(data=request_data)
        user: User = self._registration_service.register(data=user_data)

        return user


class AuthAppService(AbstractAppService):
    def __init__(self, auth_service: AuthService, token_service: TokenService):
        self._auth_service = auth_service
        self._token_service = token_service

    def _check_user_existence(self, credentials_raw: dict[str, str]) -> None:
        """
        :raises KeyError: If missing email field.
        :raises UserNotFoundException:
        """
        email: Email = request_data_to_email(credentials_raw)
        self._auth_service.check_user_existence(email)

    def login(self, credentials_raw: dict[str, str]) -> TokenPairDto:
        """
        :raises MissingRequiredFieldException: If required fields missing.
        :raises UserNotFoundException:
        :raises EmptyStringException:
        :raises InvalidEmailException:
        :raises PasswordValidationException:
        :raises pydantic.ValidationError: If fields has incorrect types
        :raises InvalidCredentialsException:
        """
        self._check_user_existence(credentials_raw=credentials_raw)

        credentials: LoginCredentials = request_data_to_login_credentials(data=credentials_raw)
        logger.info("Credentials parsed successfully")

        token_pair_vo: TokenPairVo = self._auth_service.login(credentials=credentials)
        token_pair_dto: TokenPairDto = token_pair_to_dto(token_pair_vo)

        return token_pair_dto

    def reissue_access(self, cookies: dict[str, str]) -> AccessTokenDto:
        """
        :raises ValidationException:
        :raises InvalidTokenException:
        """
        refresh_token: RefreshTokenVo = request_cookies_to_refresh_token(cookies)
        access_token: AccessTokenVo = self._auth_service.reissue_access(refresh_token)
        logger.debug("Access token issued successfully.")

        access_token_dto = access_token_to_dto(access_token)
        return access_token_dto

    def verify_access(self, cookies: dict[str, str]) -> AccessPayloadDto:
        """
        :raises MissingAccessTokenException:
        :raises InvalidTokenException:
        :raises TokenExpiredException:
        """
        access_token: AccessTokenVo = request_cookies_to_access_token(cookies)
        access_payload: AccessPayload = self._token_service.verify_access(access_token)
        logger.debug("Access token verified successfully.")

        access_payload_dto: AccessPayloadDto = access_payload_to_dto(access_payload)
        return access_payload_dto
