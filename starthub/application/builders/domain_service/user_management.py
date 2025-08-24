from application.builders.domain_service.permission import PermissionServiceBuilder
from application.ports.domain_service_builder import AbstractDomainServiceBuilder
from domain.services.file import ImageService
from domain.services.users_management.admin import UserAdminService
from domain.services.users_management.user import UserService
from domain.services.users_management.user_favorite import UserFavoriteService
from infrastructure.cloud_storages.google import google_cloud_storage
from infrastructure.repositories.project.project import DjProjectReadRepository
from infrastructure.repositories.user_management.user import (
    DjUserPhoneReadRepository,
    DjUserPhoneWriteRepository,
    DjUserReadRepository,
    DjUserWriteRepository,
)
from infrastructure.repositories.user_management.user_favorite import (
    DjUserFavoriteReadRepository,
    DjUserFavoriteWriteRepository,
)


class UserServiceBuilder(AbstractDomainServiceBuilder[UserService]):
    @staticmethod
    def create_service() -> UserService:
        return UserService(
            cloud_storage=google_cloud_storage,
            user_read_repository=DjUserReadRepository(),
            user_write_repository=DjUserWriteRepository(),
            user_phone_write_repository=DjUserPhoneWriteRepository(),
            user_phone_read_repository=DjUserPhoneReadRepository(),
            image_service=ImageService(),
        )


class UserFavoriteServiceBuilder(AbstractDomainServiceBuilder[UserFavoriteService]):
    @staticmethod
    def create_service() -> UserFavoriteService:
        return UserFavoriteService(
            user_favorite_read_repository=DjUserFavoriteReadRepository(),
            user_favorite_write_repository=DjUserFavoriteWriteRepository(),
            user_read_repository=DjUserReadRepository(),
            project_read_repository=DjProjectReadRepository(),
        )


class UserAdminServiceBuilder(AbstractDomainServiceBuilder[UserAdminService]):
    @staticmethod
    def create_service() -> UserAdminService:
        return UserAdminService(
            permission_service=PermissionServiceBuilder.create_service(), user_write_repository=DjUserWriteRepository()
        )
