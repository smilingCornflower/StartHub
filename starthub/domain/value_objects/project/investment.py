from domain.ports.command import BaseCommand
from domain.ports.payload import AbstractCreatePayload
from domain.value_objects.common import Id, LongString, PositiveNumber, SocialLink
from domain.value_objects.geo import AddressUpdatePayload


class ProjectInvestmentId(Id):
    pass


class ProjectInvestmentOrganizationName(LongString):
    pass


class ProjectInvestmentAmount(PositiveNumber):
    pass


class ProjectInvestmentCreatePayload(AbstractCreatePayload):
    project_id: Id
    organization_name: ProjectInvestmentOrganizationName
    amount: ProjectInvestmentAmount


class ProjectInvestmentUpdatePayload(AddressUpdatePayload):
    pass


class ProjectInvestmentCreateCommand(BaseCommand):
    organization_name: ProjectInvestmentOrganizationName
    amount: ProjectInvestmentAmount
    social_links: list[SocialLink]
