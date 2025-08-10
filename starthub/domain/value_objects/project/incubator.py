from domain.ports.command import BaseCommand
from domain.ports.payload import AbstractCreatePayload
from domain.value_objects.common import Description, Id, LongString
from domain.value_objects.geo import AddressUpdatePayload


class IncubatorId(Id):
    pass


class IncubatorName(LongString):
    pass


class IncubatorCreateCommand(BaseCommand):
    name: IncubatorName
    description: Description


class IncubatorCreatePayload(AbstractCreatePayload):
    project_id: Id
    name: IncubatorName
    description: Description


class IncubatorUpdatePayload(AddressUpdatePayload):
    project_id: Id
    name: IncubatorName
    description: Description
