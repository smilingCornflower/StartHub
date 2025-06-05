from typing import BinaryIO

from domain.ports.payload import AbstractCreatePayload, AbstractDeletePayload, AbstractUpdatePayload


class CloudStorageUploadPayload(AbstractCreatePayload):
    file_obj: BinaryIO
    file_path: str


class CloudStorageUpdatePayload(AbstractUpdatePayload):
    pass


class CloudStorageDeletePayload(AbstractDeletePayload):
    file_path: str


class CloudStorageCreateUrlPayload(AbstractCreatePayload):
    file_path: str
