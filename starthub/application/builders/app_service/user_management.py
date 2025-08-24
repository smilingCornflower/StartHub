from application.builders.domain_service.project_management import ProjectServiceBuilder
from application.builders.domain_service.user_management import (
    UserAdminServiceBuilder,
    UserFavoriteServiceBuilder,
    UserMessageServiceBuilder,
    UserServiceBuilder,
)
from application.ports.app_service_builder import AbstractAppServiceBuilder
from application.services.user_management.user import UserAppService
from application.services.user_management.user_admin import UserAdminAppService
from application.services.user_management.user_favorite import UserFavoriteAppService
from application.services.user_management.user_message import UserMessageAppService
from infrastructure.repositories.project.category import DjProjectCategoryReadRepository
from infrastructure.repositories.project.project import DjProjectReadRepository
from infrastructure.repositories.role import DjRoleReadRepository
from infrastructure.repositories.user_management.user import DjUserReadRepository
from infrastructure.repositories.user_management.user_message import DjUserMessageReadRepository


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


class UserFavoriteAppAppServiceBuilder(AbstractAppServiceBuilder[UserFavoriteAppService]):
    @staticmethod
    def create_service() -> UserFavoriteAppService:
        return UserFavoriteAppService(
            user_favorite_service=UserFavoriteServiceBuilder.create_service(),
            project_read_repository=DjProjectReadRepository(),
            project_category_read_repository=DjProjectCategoryReadRepository(),
            project_service=ProjectServiceBuilder.create_service(),
        )


class UserMessageAppServiceBuilder(AbstractAppServiceBuilder[UserMessageAppService]):
    @staticmethod
    def create_service() -> UserMessageAppService:
        return UserMessageAppService(
            user_message_service=UserMessageServiceBuilder.create_service(),
            user_read_repository=DjUserReadRepository(),
            user_message_read_repository=DjUserMessageReadRepository(),
        )
