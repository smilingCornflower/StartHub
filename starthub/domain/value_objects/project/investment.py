from pydantic import field_validator

from domain.constants import PROJECT_INVESTMENTS_PHONE_MAX_AMOUNT
from domain.exceptions.project_management import ProjectInvestmentPhoneMaxAmountException
from domain.ports.command import BaseCommand
from domain.ports.payload import AbstractCreatePayload
from domain.value_objects.common import Id, LongString, PhoneNumber, PositiveNumber, SocialLink
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
    investment_id: Id
    organization_name: ProjectInvestmentOrganizationName | None = None
    amount: ProjectInvestmentAmount | None = None


class ProjectInvestmentCreateCommand(BaseCommand):
    organization_name: ProjectInvestmentOrganizationName
    amount: ProjectInvestmentAmount
    social_links: list[SocialLink]
    phone_numbers: list[PhoneNumber]

    @field_validator("phone_numbers", mode="after")
    @classmethod
    def check_max_amount(cls, phone_numbers: list[PhoneNumber]) -> list[PhoneNumber]:
        """:raises ProjectInvestmentPhoneMaxAmountException:"""

        if not (len(phone_numbers) < PROJECT_INVESTMENTS_PHONE_MAX_AMOUNT):
            raise ProjectInvestmentPhoneMaxAmountException(
                f"Maximum number of phones ({PROJECT_INVESTMENTS_PHONE_MAX_AMOUNT}) has been reached"
            )
        return phone_numbers


class ProjectInvestmentUpdateCommand(BaseCommand):
    organization_name: ProjectInvestmentOrganizationName | None = None
    amount: ProjectInvestmentAmount | None = None
    social_links: list[SocialLink] | None = None
