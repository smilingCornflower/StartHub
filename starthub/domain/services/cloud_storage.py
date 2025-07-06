from domain.ports.cloud_storage import AbstractCloudStorage
from domain.ports.service import AbstractDomainService
from domain.value_objects.cloud_storage import (
    CloudStorageCreateUrlPayload,
    CloudStorageDeletePayload,
    CloudStorageUploadPayload,
)


class StorageService(AbstractDomainService):
    def __init__(self, cloud_storage: AbstractCloudStorage):
        self._cloud_storage = cloud_storage

    def upload_file(self, payload: CloudStorageUploadPayload) -> str:
        return self._cloud_storage.upload_file(payload=payload)

    def delete_file(self, payload: CloudStorageDeletePayload) -> None:
        """:raises NotImplementedError:"""
        return self._cloud_storage.delete_file(payload=payload)

    def create_url(self, payload: CloudStorageCreateUrlPayload) -> str:
        """:raises NotImplementedError:"""
        return self._cloud_storage.create_url(payload=payload)
