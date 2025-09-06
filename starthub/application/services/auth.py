from application.converters.resposne_converters.auth import (
    access_payload_to_dto,
    access_token_to_dto,
    anonymous_payload_to_dto,
    token_pair_to_dto,
)
from application.dto.auth import AccessPayloadDto, AccessTokenDto, AnonymousPayloadDto, AnonymousTokenDto, TokenPairDto
from application.ports.service import AbstractAppService
from domain.models.user_management.user import User
from domain.repositories.user_management.user import UserReadRepository
from domain.services.auth import AuthService, RegistrationService, TokenService
from domain.value_objects.auth_management.auth import LoginCredentials
from domain.value_objects.auth_management.token import (
    AccessPayload,
    AccessTokenVo,
    AnonymousPayload,
    AnonymousTokenVo,
    RefreshTokenVo,
    TokenPairVo,
)
from domain.value_objects.common import Id
from domain.value_objects.user_management.anonymous import AnonymousId, AnonymousUser
from domain.value_objects.user_management.user import UserCreatePayload
from loguru import logger
from presentation.request_converters.user_management.auth import (
    request_cookies_to_refresh_token,
    request_data_to_login_credentials,
    request_data_to_user_create_payload,
)


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
    def __init__(
        self, auth_service: AuthService, token_service: TokenService, user_read_repository: UserReadRepository
    ):
        self._auth_service = auth_service
        self._token_service = token_service
        self._user_read_repository = user_read_repository

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

    def generate_anonymous(self) -> AnonymousTokenDto:
        token: AnonymousTokenVo = self._token_service.generate_anonymous()
        return AnonymousTokenDto(anonymous_token=token.value)

    def verify_anonymous_token(self, token: AnonymousTokenVo) -> AnonymousPayloadDto:
        payload: AnonymousPayload = self._token_service.verify_anonymous(token=token)
        return anonymous_payload_to_dto(anonymous_payload=payload)

    def verify_access_token(self, token: AccessTokenVo) -> AccessPayloadDto:
        payload: AccessPayload = self._token_service.verify_access(token=token)
        return access_payload_to_dto(access_payload=payload)

    def get_authenticated_user(self, token: AccessTokenVo) -> User:
        """:raises UserDeactivedException:"""

        payload: AccessPayload = self._token_service.verify_access(token=token)
        user_id = Id(value=int(payload.sub))
        user = self._user_read_repository.get_by_id(id_=user_id)
        return self._auth_service.verify_user_access(user=user)

    def get_anonymous_user(self, token: AnonymousTokenVo) -> AnonymousUser:
        payload: AnonymousPayload = self._token_service.verify_anonymous(token=token)
        anonymous_id = AnonymousId(value=payload.sub)
        return AnonymousUser(id=anonymous_id)

    def get_authenticated_or_anonymous_user(self, token: AccessTokenVo | AnonymousTokenVo) -> User | AnonymousUser:
        if isinstance(token, AccessTokenVo):
            return self.get_authenticated_user(token=token)
        else:
            return self.get_anonymous_user(token=token)
