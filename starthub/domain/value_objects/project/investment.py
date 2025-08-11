from domain.ports.payload import AbstractCreatePayload
from domain.value_objects.common import Id
from domain.value_objects.geo import AddressUpdatePayload


class ProjectInvestmentId(Id):
    pass


class ProjectInvestmentCreatePayload(AbstractCreatePayload):
    pass


class ProjectInvestmentUpdatePayload(AddressUpdatePayload):
    pass
