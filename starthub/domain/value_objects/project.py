from datetime import date

from domain.constants import CHAR_FIELD_MAX_LENGTH
from domain.exceptions.project import (
    NegativeProjectGoalSumValidationException,
    ProjectDeadlineInPastValidationException,
    ProjectNameIsTooLongValidationException,
)
from domain.exceptions.validation import EmptyStringException
from domain.ports.payload import AbstractCreatePayload, AbstractUpdatePayload
from domain.validators.business_number import KZBusinessNumberValidator
from domain.value_objects.base import BaseVo
from domain.value_objects.common import Id, PhoneNumber, SocialLink
from domain.value_objects.country import CountryCode
from domain.value_objects.team_member import TeamMemberInProjectCreatePayload
from pydantic import ValidationInfo, field_validator


class BusinessNumber(BaseVo):
    country_code: CountryCode
    value: str

    @field_validator("value", mode="after")
    @classmethod
    def is_correct_business_number(cls, value: str, info: ValidationInfo) -> str:
        """:raises ValidationException:"""
        if info.data.get("country_code") and info.data["country_code"].value == "KZ":
            KZBusinessNumberValidator.validate(value)
        return value


class ProjectCreatePayload(AbstractCreatePayload, BaseVo):
    name: str
    description: str
    category_id: Id
    creator_id: Id
    funding_model_id: Id
    goal_sum: float
    deadline: date
    team_members: list[TeamMemberInProjectCreatePayload]
    company_id: Id
    social_links: list[SocialLink]
    phone_number: PhoneNumber

    @field_validator("name", mode="after")
    @classmethod
    def is_valid_name(cls, value: str) -> str:
        """:raises ProjectNameIsTooLongValidationException:"""
        if not value:
            raise EmptyStringException("Project name cannot be empty.")
        if len(value) > CHAR_FIELD_MAX_LENGTH:
            raise ProjectNameIsTooLongValidationException(
                f"Project name must be at most {CHAR_FIELD_MAX_LENGTH} characters long."
            )
        return value

    @field_validator("goal_sum", mode="after")
    @classmethod
    def is_positive(cls, value: int) -> int:
        """:raises NegativeProjectGoalSumValidationException:"""
        if value <= 0:
            raise NegativeProjectGoalSumValidationException("goal_sum must be positive.")
        return value

    @field_validator("deadline", mode="after")
    @classmethod
    def deadline_in_future(cls, value: date) -> date:
        """:raises ProjectDeadlineInPastValidationException:"""
        if value <= date.today():
            raise ProjectDeadlineInPastValidationException("deadline must be in the future.")
        return value


class ProjectUpdatePayload(AbstractUpdatePayload, BaseVo):
    id_: Id
    name: str | None
    description: str | None
    category_id: Id | None
    funding_model_id: Id | None
    goal_sum: float | None
    deadline: date | None
