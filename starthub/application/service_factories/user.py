from application.ports.service_factory import AbstractAppServiceFactory
from application.services.user import UserAppService
from domain.services.file import ImageService
from domain.services.user import UserService
from infrastructure.cloud_storages.google import google_cloud_storage
from infrastructure.repositories.user import DjUserReadRepository, DjUserWriteRepository


class UserAppServiceFactory(AbstractAppServiceFactory[UserAppService]):
    @staticmethod
    def create_service() -> UserAppService:
        return UserAppService(
            user_service=UserService(
                cloud_storage=google_cloud_storage,
                user_read_repository=DjUserReadRepository(),
                user_write_repository=DjUserWriteRepository(),
                image_service=ImageService(),
            )
        )
