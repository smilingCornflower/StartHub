from application.builders.domain_service.user import UserServiceBuilder
from application.ports.app_service_builder import AbstractAppServiceBuilder
from application.services.user import UserAppService


class UserAppServiceBuilder(AbstractAppServiceBuilder[UserAppService]):
    @staticmethod
    def create_service() -> UserAppService:
        return UserAppService(
            user_service=UserServiceBuilder.create_service(),
        )
