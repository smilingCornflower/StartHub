from application.builders.domain_service.user_management import UserAdminServiceBuilder, UserServiceBuilder
from application.ports.app_service_builder import AbstractAppServiceBuilder
from application.services.user_management.admin import UserAdminAppService
from application.services.user_management.user import UserAppService
from infrastructure.repositories.role import DjRoleReadRepository
from infrastructure.repositories.user_management.user import DjUserReadRepository


class UserAppServiceBuilder(AbstractAppServiceBuilder[UserAppService]):
    @staticmethod
    def create_service() -> UserAppService:
        return UserAppService(
            user_service=UserServiceBuilder.create_service(),
        )


class UserAdminAppServiceBuilder(AbstractAppServiceBuilder[UserAdminAppService]):
    @staticmethod
    def create_service() -> UserAdminAppService:
        return UserAdminAppService(
            user_admin_service=UserAdminServiceBuilder.create_service(),
            user_read_repository=DjUserReadRepository(),
            role_read_repository=DjRoleReadRepository(),
        )
