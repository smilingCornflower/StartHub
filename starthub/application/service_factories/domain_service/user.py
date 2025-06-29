from application.ports.domain_service_factory import AbstractDomainServiceFactory
from domain.services.file import ImageService
from domain.services.user_management import UserService
from infrastructure.cloud_storages.google import google_cloud_storage
from infrastructure.repositories.user import (
    DjUserPhoneReadRepository,
    DjUserPhoneWriteRepository,
    DjUserReadRepository,
    DjUserWriteRepository,
)


class UserServiceFactory(AbstractDomainServiceFactory[UserService]):
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
