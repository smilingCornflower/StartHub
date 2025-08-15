from domain.ports.command import BaseCommand
from domain.ports.payload import AbstractCreatePayload, AbstractUpdatePayload
from domain.value_objects.common import Id
from domain.value_objects.file import FileVo


class MediaFile(FileVo):
    pass


class ProjectMediaId(Id):
    pass


class ProjectMediaCreatePayload(AbstractCreatePayload):
    project_id: Id
    file_path: str
    order: int


class ProjectMediaUpdatePayload(AbstractUpdatePayload):
    pass


class ProjectMediaCreateCommand(BaseCommand):
    media: MediaFile


class ProjectMediaUpdateCommand(BaseCommand):
    pass
