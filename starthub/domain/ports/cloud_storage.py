from abc import ABC, abstractmethod
from typing import BinaryIO


class CloudStorageInterface(ABC):
    @abstractmethod
    def upload_file(self, file_obj: BinaryIO, file_name: str) -> str:
        """
        Uploads a binary file object to cloud storage at the specified path.

        :param file_obj: A binary file-like object (e.g. an uploaded file or BytesIO).
        :param file_name: Destination path in the cloud storage (e.g. "folder/filename.ext").
        :return: The full path or identifier of the uploaded file in storage.
        """
        pass

    @abstractmethod
    def delete_file(self, file_name: str) -> None:
        pass

    @abstractmethod
    def create_url(self, file_name) -> str:
        pass
