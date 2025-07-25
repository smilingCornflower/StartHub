from application.converters.request_converters.auth import (
    request_cookies_to_refresh_token,
    request_data_to_login_credentials,
    request_data_to_user_create_payload,
    request_headers_to_access_token,
    request_headers_to_anonymous_token,
)
from application.converters.resposne_converters.auth import (
    access_payload_to_dto,
    access_token_to_dto,
    anonymous_payload_to_dto,
    token_pair_to_dto,
)
from application.dto.auth import AccessPayloadDto, AccessTokenDto, AnonymousPayloadDto, AnonymousTokenDto, TokenPairDto
from application.ports.service import AbstractAppService
from domain.models.user import User
from domain.services.auth import AuthService, RegistrationService, TokenService
from domain.value_objects.auth import LoginCredentials
from domain.value_objects.token import (
    AccessPayload,
    AccessTokenVo,
    AnonymousPayload,
    AnonymousTokenVo,
    RefreshTokenVo,
    TokenPairVo,
)
from domain.value_objects.user import UserCreatePayload
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
        credentials: LoginCredentials = request_data_to_login_credentials(data=credentials_raw)
        logger.info("Credentials parsed successfully")

        token_pair_vo: TokenPairVo = self._auth_service.login(credentials=credentials)
        token_pair_dto: TokenPairDto = token_pair_to_dto(token_pair_vo)

        return token_pair_dto

    def reissue_access(self, cookies: dict[str, str]) -> AccessTokenDto:
        """
        :raises MissingRequiredFieldException:
        :raises ValidationException:
        :raises InvalidTokenException:
        """
        refresh_token: RefreshTokenVo = request_cookies_to_refresh_token(cookies)
        access_token: AccessTokenVo = self._auth_service.reissue_access(refresh_token)
        logger.debug("Access token issued successfully.")

        access_token_dto = access_token_to_dto(access_token)
        return access_token_dto

    def verify_access_from_headers(self, headers: dict[str, str]) -> AccessPayloadDto:
        """
        :raises MissingRequiredFieldException:
        :raises pydantic.ValidationError:
        :raises InvalidTokenException:
        :raises TokenExpiredException:
        """
        access_token: AccessTokenVo = request_headers_to_access_token(headers=headers)
        access_payload: AccessPayload = self._token_service.verify_access(token=access_token)
        return access_payload_to_dto(access_payload)

    def generate_anonymous(self) -> AnonymousTokenDto:
        token: AnonymousTokenVo = self._token_service.generate_anonymous()
        return AnonymousTokenDto(anonymous_token=token.value)

    def verify_anonymous_from_headers(self, headers: dict[str, str]) -> AnonymousPayloadDto:
        """
        :raises MissingRequiredFieldException:
        :raises pydantic.ValidationError:
        :raises InvalidTokenException:
        :raises TokenExpiredException:
        """
        anonymous_token: AnonymousTokenVo = request_headers_to_anonymous_token(headers=headers)
        anonymous_payload: AnonymousPayload = self._token_service.verify_anonymous(token=anonymous_token)
        return anonymous_payload_to_dto(anonymous_payload=anonymous_payload)
