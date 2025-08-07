from domain.ports.command import BaseCommand
from domain.value_objects.common import Id, LongString, Description


class IncubatorId(Id):
    pass


class IncubatorName(LongString):
    pass


class IncubatorCreateCommand(BaseCommand):
    name: IncubatorName
    description: Description


class IncubatorCreatePayload(BaseCommand):
    project_id: Id
    name: IncubatorName
    description: Description
