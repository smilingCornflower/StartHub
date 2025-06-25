from application.ports.domain_service_factory import AbstractDomainServiceFactory
from config import settings
from domain.services.auth import AuthService, RegistrationService, TokenService
from infrastructure.repositories.user import DjUserReadRepository, DjUserWriteRepository


class AuthServiceFactory(AbstractDomainServiceFactory[AuthService]):
    @staticmethod
    def create_service() -> AuthService:
        return AuthService(
            token_service=TokenService(secret_key=settings.SECRET_KEY),
            user_read_repository=DjUserReadRepository(),
            user_write_repository=DjUserWriteRepository(),
        )


class TokenServiceFactory(AbstractDomainServiceFactory[TokenService]):
    @staticmethod
    def create_service() -> TokenService:
        return TokenService(secret_key=settings.SECRET_KEY)


class RegistrationServiceFactory(AbstractDomainServiceFactory[RegistrationService]):
    @staticmethod
    def create_service() -> RegistrationService:
        return RegistrationService(
            read_repository=DjUserReadRepository(),
            write_repository=DjUserWriteRepository(),
        )
