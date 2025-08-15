from domain.ports.command import BaseCommand
from domain.ports.payload import AbstractCreatePayload, AbstractUpdatePayload
from domain.value_objects.common import Id, LongString
from domain.value_objects.file import FileVo


class ProjectFileId(Id):
    pass


class ProjectFileName(LongString):
    pass


class ProjectFileCreatePayload(AbstractCreatePayload):
    project_id: Id
    file_path: str
    name: ProjectFileName | None


class ProjectFileUpdatePayload(AbstractUpdatePayload):
    pass


class ProjectFileCreateCommand(BaseCommand):
    file: FileVo
    name: ProjectFileName | None = None
