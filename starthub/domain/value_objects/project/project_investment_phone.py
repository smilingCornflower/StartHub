from domain.ports.payload import AbstractCreatePayload
from domain.value_objects.common import Id, PhoneNumber
from domain.value_objects.geo import AddressUpdatePayload
from domain.value_objects.project.investment import ProjectInvestmentId


class ProjectInvestmentPhoneId(Id):
    pass


class ProjectInvestmentPhoneCreatePayload(AbstractCreatePayload):
    investment_id: ProjectInvestmentId
    phone_number: PhoneNumber


class ProjectInvestmentPhoneUpdatePayload(AddressUpdatePayload):
    pass
