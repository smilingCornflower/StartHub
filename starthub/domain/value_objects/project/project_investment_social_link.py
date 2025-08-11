from domain.ports.payload import AbstractCreatePayload
from domain.value_objects.common import Id
from domain.value_objects.geo import AddressUpdatePayload


class ProjectInvestmentSocialLinkId(Id):
    pass


class ProjectInvestmentSocialLinkCreatePayload(AbstractCreatePayload):
    pass


class ProjectInvestmentSocialLinkUpdatePayload(AddressUpdatePayload):
    pass
