from domain.ports.cloud_storage import AbstractCloudStorage
from domain.ports.service import AbstractDomainService
from domain.value_objects.cloud_storage import (
    CloudStorageCreateUrlPayload,
    CloudStorageDeletePayload,
    CloudStorageUploadPayload,
)


class CloudService(AbstractDomainService):
    def __init__(self, cloud_storage: AbstractCloudStorage):
        self._cloud_storage = cloud_storage

    def upload_file(self, payload: CloudStorageUploadPayload) -> str:
        file_path: str = self._cloud_storage.upload_file(payload=payload)
        return file_path

    def delete_file(self, payload: CloudStorageDeletePayload) -> None:
        """:raises NotImplementedError:"""
        raise NotImplementedError("The method delete_file() is not implemented yet.")

    def create_url(self, payload: CloudStorageCreateUrlPayload) -> str:
        """:raises NotImplementedError:"""
        raise NotImplementedError("The method update_file() is not implemented yet.")
