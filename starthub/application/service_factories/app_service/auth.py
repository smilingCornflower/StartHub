from application.ports.app_service_factory import AbstractAppServiceFactory
from application.service_factories.domain_service.auth import (
    AuthServiceBuilder,
    RegistrationServiceBuilder,
    TokenServiceBuilder,
)
from application.services.auth import AuthAppService, RegistrationAppService


class AuthAppServiceFactory(AbstractAppServiceFactory[AuthAppService]):
    @staticmethod
    def create_service() -> AuthAppService:
        return AuthAppService(
            token_service=TokenServiceBuilder.create_service(),
            auth_service=AuthServiceBuilder.create_service(),
        )


class RegistrationAppServiceFactory(AbstractAppServiceFactory[RegistrationAppService]):
    @staticmethod
    def create_service() -> RegistrationAppService:
        return RegistrationAppService(registration_service=RegistrationServiceBuilder.create_service())


auth_app_service: AuthAppService = AuthAppServiceFactory.create_service()
registration_app_service: RegistrationAppService = RegistrationAppServiceFactory.create_service()
