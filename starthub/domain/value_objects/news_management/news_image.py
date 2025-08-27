from domain.ports.command import BaseCommand
from domain.ports.payload import AbstractCreatePayload, AbstractDeletePayload, AbstractUpdatePayload
from domain.value_objects.common import Id
from domain.value_objects.file import ImageFile


class NewsImageUploadCommand(BaseCommand):
    image: ImageFile


class NewsImageCreatePayload(AbstractCreatePayload):
    news_id: Id
    image: str


class NewsImageUpdatePayload(AbstractUpdatePayload):
    pass


class NewsImageDeletePayload(AbstractDeletePayload):
    file_name: str
