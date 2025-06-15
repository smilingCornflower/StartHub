from abc import ABC, abstractmethod

from domain.value_objects.cloud_storage import (
    CloudStorageCreateUrlPayload,
    CloudStorageDeletePayload,
    CloudStorageUploadPayload,
)


class AbstractCloudStorage(ABC):
    @abstractmethod
    def upload_file(self, payload: CloudStorageUploadPayload) -> str:
        """:returns: The path to uploaded file in the cloud storage."""
        pass

    @abstractmethod
    def delete_file(self, payload: CloudStorageDeletePayload) -> None:
        """:raises FileNotFoundCloudStorageException:"""
        pass

    @abstractmethod
    def create_url(self, payload: CloudStorageCreateUrlPayload) -> str:
        """:return: A url that can be used to access the file."""
        pass
