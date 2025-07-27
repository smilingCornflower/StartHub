from application.ports.app_service_factory import AbstractAppServiceFactory
from application.service_factories.domain_service.user import UserServiceBuilder
from application.services.user import UserAppService


class UserAppServiceFactory(AbstractAppServiceFactory[UserAppService]):
    @staticmethod
    def create_service() -> UserAppService:
        return UserAppService(
            user_service=UserServiceBuilder.create_service(),
        )
