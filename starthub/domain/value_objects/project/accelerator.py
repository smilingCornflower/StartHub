from domain.ports.command import BaseCommand
from domain.ports.payload import AbstractCreatePayload
from domain.value_objects.common import Description, Id, MediumString
from domain.value_objects.geo import AddressUpdatePayload


class AcceleratorId(Id):
    pass


class AcceleratorName(MediumString):
    pass


class ProjectAcceleratorCreatePayload(AbstractCreatePayload):
    project_id: Id
    name: AcceleratorName
    description: Description


class ProjectAcceleratorUpdatePayload(AddressUpdatePayload):
    pass


class ProjectAcceleratorCreateCommand(BaseCommand):
    name: AcceleratorName
    description: Description
