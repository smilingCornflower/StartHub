from domain.ports.command import BaseCommand
from domain.ports.payload import AbstractCreatePayload
from domain.value_objects.common import Description, Id
from domain.value_objects.geo import AddressUpdatePayload


class ProjectBootstrapId(Id):
    pass


class ProjectBootstrapCreatePayload(AbstractCreatePayload):
    project_id: Id
    description: Description


class ProjectBootstrapUpdatePayload(AddressUpdatePayload):
    bootstrap_id: ProjectBootstrapId
    description: Description | None = None


class ProjectBootstrapCreateCommand(BaseCommand):
    description: Description


class ProjectBootstrapUpdateCommand(BaseCommand):
    description: Description | None
