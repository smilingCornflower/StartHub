from application.ports.domain_service_builder import AbstractDomainServiceBuilder
from config import settings
from domain.services.auth import AuthService, RegistrationService, TokenService
from infrastructure.repositories.role import DjRoleReadRepository
from infrastructure.repositories.user import DjUserReadRepository, DjUserWriteRepository


class AuthServiceBuilder(AbstractDomainServiceBuilder[AuthService]):
    @staticmethod
    def create_service() -> AuthService:
        return AuthService(
            token_service=TokenService(secret_key=settings.SECRET_KEY, role_read_repository=DjRoleReadRepository()),
            user_read_repository=DjUserReadRepository(),
            user_write_repository=DjUserWriteRepository(),
        )


class TokenServiceBuilder(AbstractDomainServiceBuilder[TokenService]):
    @staticmethod
    def create_service() -> TokenService:
        return TokenService(secret_key=settings.SECRET_KEY, role_read_repository=DjRoleReadRepository())


class RegistrationServiceBuilder(AbstractDomainServiceBuilder[RegistrationService]):
    @staticmethod
    def create_service() -> RegistrationService:
        return RegistrationService(
            read_repository=DjUserReadRepository(),
            write_repository=DjUserWriteRepository(),
        )
