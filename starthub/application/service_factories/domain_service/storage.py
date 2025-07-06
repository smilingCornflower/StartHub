from application.ports.domain_service_factory import AbstractDomainServiceFactory
from domain.services.cloud_storage import StorageService
from infrastructure.cloud_storages.google import google_cloud_storage


class StorageServiceFactory(AbstractDomainServiceFactory[StorageService]):
    @staticmethod
    def create_service() -> StorageService:
        return StorageService(cloud_storage=google_cloud_storage)
