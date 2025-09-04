from application.builders.domain_service.auth import AuthServiceBuilder, RegistrationServiceBuilder, TokenServiceBuilder
from application.ports.app_service_builder import AbstractAppServiceBuilder
from application.services.auth import AuthAppService, RegistrationAppService
from infrastructure.repositories.user_management.user import DjUserReadRepository


class AuthAppServiceBuilder(AbstractAppServiceBuilder[AuthAppService]):
    @staticmethod
    def create_service() -> AuthAppService:
        return AuthAppService(
            token_service=TokenServiceBuilder.create_service(),
            auth_service=AuthServiceBuilder.create_service(),
            user_read_repository=DjUserReadRepository(),
        )


class RegistrationAppServiceBuilder(AbstractAppServiceBuilder[RegistrationAppService]):
    @staticmethod
    def create_service() -> RegistrationAppService:
        return RegistrationAppService(registration_service=RegistrationServiceBuilder.create_service())


auth_app_service: AuthAppService = AuthAppServiceBuilder.create_service()
registration_app_service: RegistrationAppService = RegistrationAppServiceBuilder.create_service()
