from domain.ports.command import BaseCommand
from domain.ports.payload import AbstractCreatePayload, AbstractUpdatePayload
from domain.value_objects.common import Description, Id


class ProjectStageId(Id):
    pass


class ProjectStageCreatePayload(AbstractCreatePayload):
    pass


class ProjectStageUpdatePayload(AbstractUpdatePayload):
    id_: ProjectStageId
    description: Description | None


class ProjectStageUpdateCommand(BaseCommand):
    description: Description | None
