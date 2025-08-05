from application.ports.domain_service_builder import AbstractDomainServiceBuilder
from domain.services.cloud_storage import StorageService
from infrastructure.cloud_storages.google import google_cloud_storage


class StorageServiceBuilder(AbstractDomainServiceBuilder[StorageService]):
    @staticmethod
    def create_service() -> StorageService:
        return StorageService(cloud_storage=google_cloud_storage)
