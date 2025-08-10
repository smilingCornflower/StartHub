from domain.constants import PROJECT_CROWDFUNDING_AMOUNT_MAX_DIGITS
from domain.exceptions.project_management import ProjectCrowdfundingMaxAmountException
from domain.ports.command import BaseCommand
from domain.ports.payload import AbstractCreatePayload
from domain.value_objects.common import Id, LongString, PositiveNumber
from domain.value_objects.geo import AddressUpdatePayload
from pydantic import field_validator


class ProjectCrowdfundingId(Id):
    pass


class ProjectCrowdfundingName(LongString):
    pass


class ProjectCrowdfundingAmount(PositiveNumber):
    @field_validator("value", mode="after")
    @classmethod
    def validate_funding_max_amount(cls, value: float) -> float:
        """:raises ProjectCrowdfundingMaxAmountException:"""
        if value >= 10**PROJECT_CROWDFUNDING_AMOUNT_MAX_DIGITS:
            raise ProjectCrowdfundingMaxAmountException(
                f"Funding amount {value} exceeds maximum allowed {PROJECT_CROWDFUNDING_AMOUNT_MAX_DIGITS}"
            )
        return value


class ProjectCrowdfundingCreatePayload(AbstractCreatePayload):
    project_id: Id
    name: ProjectCrowdfundingName
    amount: ProjectCrowdfundingAmount


class ProjectCrowdfundingUpdatePayload(AddressUpdatePayload):
    project_id: Id
    name: ProjectCrowdfundingName
    amount: ProjectCrowdfundingAmount


class ProjectCrowdfundingCreateCommand(BaseCommand):
    name: ProjectCrowdfundingName
    amount: ProjectCrowdfundingAmount
