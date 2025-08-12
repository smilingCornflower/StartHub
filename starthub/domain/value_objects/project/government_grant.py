from domain.ports.command import BaseCommand
from domain.ports.payload import AbstractCreatePayload
from domain.value_objects.common import Id, LongString, PositiveNumber
from domain.value_objects.geo import AddressUpdatePayload


class ProjectGovernmentGrantId(Id):
    pass


class ProjectGrantName(LongString):
    pass


class ProjectGrantOrganizationName(LongString):
    pass


class ProjectGovernmentGrantAmount(PositiveNumber):
    pass


class ProjectGoverntmentGrantCreatePayload(AbstractCreatePayload):
    project_id: Id
    grant_name: ProjectGrantName
    organization_name: ProjectGrantOrganizationName
    amount: ProjectGovernmentGrantAmount


class ProjectGovernmentGrantUpdatePayload(AddressUpdatePayload):
    pass


class ProjectGoverntmentGrantCreateCommand(BaseCommand):
    grant_name: ProjectGrantName
    organization_name: ProjectGrantOrganizationName
    amount: ProjectGovernmentGrantAmount


class ProjectGoverntmentGrantUpdateCommand(BaseCommand):
    pass
