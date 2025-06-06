from domain.ports.payload import AbstractCreatePayload, AbstractDeletePayload, AbstractUpdatePayload
from domain.value_objects import BaseVo


class CloudStorageUploadPayload(AbstractCreatePayload, BaseVo):
    file_data: bytes
    file_path: str


class CloudStorageUpdatePayload(AbstractUpdatePayload, BaseVo):
    pass


class CloudStorageDeletePayload(AbstractDeletePayload, BaseVo):
    file_path: str


class CloudStorageCreateUrlPayload(AbstractCreatePayload, BaseVo):
    file_path: str
