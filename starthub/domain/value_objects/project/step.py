from domain.ports.command import BaseCommand
from domain.ports.payload import AbstractCreatePayload
from domain.value_objects.common import DeadlineDate, Description, Id, MediumString
from domain.value_objects.geo import AddressUpdatePayload


class ProjectStepId(Id):
    pass


class ProjectStepName(MediumString):
    pass


class ProjectStepDate(DeadlineDate):
    pass


class ProjectStepCreateCommand(BaseCommand):
    name: ProjectStepName
    description: Description
    date: ProjectStepDate


class ProjectStepCreatePaylaod(AbstractCreatePayload):
    project_id: Id
    name: ProjectStepName
    description: Description
    date: ProjectStepDate


class ProjectStepUpdatePayload(AddressUpdatePayload):
    pass
