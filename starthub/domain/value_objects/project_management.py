from datetime import date

from domain.constants import CHAR_FIELD_MAX_LENGTH
from domain.exceptions.project_management import (
    NegativeProjectGoalSumValidationException,
    ProjectDeadlineInPastValidationException,
    ProjectNameIsTooLongValidationException,
)
from domain.exceptions.validation import EmptyStringException
from domain.ports.payload import AbstractCreatePayload, AbstractUpdatePayload
from domain.value_objects import BaseVo
from domain.value_objects.common import FirstName, Id, LastName, PhoneNumber, SocialLink
from pydantic import field_validator


class ProjectPhoneCreatePayload(AbstractCreatePayload, BaseVo):
    project_id: Id
    number: PhoneNumber


class ProjectPhoneUpdatePayload(AbstractUpdatePayload, BaseVo):
    phone_id: Id
    number: PhoneNumber


class ProjectSocialLinkCreatePayload(AbstractCreatePayload, BaseVo):
    project_id: Id
    social_link: SocialLink


class ProjectSocialLinkUpdatePayload(AbstractUpdatePayload, BaseVo):
    project_id: Id
    social_link: SocialLink


class TeamMemberCreatePayload(AbstractCreatePayload, BaseVo):
    project_id: Id
    first_name: FirstName
    last_name: LastName
    description: str


class TeamMemberInProjectCreatePayload(BaseVo):
    first_name: FirstName
    last_name: LastName
    description: str


class TeamMemberUpdatePayload(AbstractUpdatePayload, BaseVo):
    pass


class ProjectCategoryCreatePayload(AbstractCreatePayload, BaseVo):
    pass


class ProjectCategoryUpdatePayload(AbstractUpdatePayload, BaseVo):
    pass


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
        """
        :raises ProjectNameIsTooLongValidationException:
        :raises EmptyStringException:
        """
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
