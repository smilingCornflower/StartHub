from domain.ports.payload import AbstractCreatePayload
from domain.value_objects.common import Id
from domain.value_objects.geo import AddressUpdatePayload


class ProjectCrowdfundingId(Id):
    pass


class ProjectCrowdfundingCreatePayload(AbstractCreatePayload):
    pass


class ProjectCrowdfundingUpdatePayload(AddressUpdatePayload):
    pass
