from datetime import date

from domain.constants import CHAR_FIELD_MAX_LENGTH
from domain.enums.project_stage import ProjectStageEnum
from domain.enums.project_status import ProjectStatusEnum
from domain.exceptions.project_management import (
    InvalidProjectStageException,
    InvalidProjectStatusException,
    NegativeProjectGoalSumException,
    ProjectNameIsTooLongException,
)
from domain.exceptions.validation import EmptyStringException
from domain.ports.command import BaseCommand
from domain.ports.payload import AbstractCreatePayload, AbstractDeletePayload, AbstractUpdatePayload
from domain.value_objects import BaseVo
from domain.value_objects.common import (
    DeadlineDate,
    Description,
    FirstName,
    Id,
    LastName,
    Order,
    PhoneNumber,
    SocialLink,
)
from domain.value_objects.company import (
    BusinessNumber,
    CompanyFounderCreateCommand,
    CompanyName,
    CompanyUpdatePayload,
    EstablishedDate,
)
from domain.value_objects.country import CountryCode
from domain.value_objects.file import ImageFile, PdfFile
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
    description: Description


class TeamMemberCreateCommand(BaseVo):
    first_name: FirstName
    last_name: LastName
    description: Description


class TeamMemberUpdatePayload(AbstractUpdatePayload, BaseVo):
    pass


class ProjectCategoryCreatePayload(AbstractCreatePayload, BaseVo):
    pass


class ProjectCategoryUpdatePayload(AbstractUpdatePayload, BaseVo):
    pass


class ProjectStage(BaseVo):
    value: str

    @field_validator("value", mode="after")
    @classmethod
    def is_valid_stage(cls, value: str) -> str:
        """:raises InvalidProjectStageException:"""

        if value.lower() not in ProjectStageEnum:
            raise InvalidProjectStageException(
                f"Invalid project stage: {value}. Allowed stages: {', '.join([stage for stage in ProjectStageEnum])}"
            )
        return value.lower()


# TODO: write tests for ProjectStatus
class ProjectStatus(BaseVo):
    value: str

    @field_validator("value", mode="after")
    @classmethod
    def is_valid_stage(cls, value: str) -> str:
        """:raises InvalidProjectStatusException:"""

        if value.lower() not in ProjectStatusEnum:
            raise InvalidProjectStatusException(
                f"Invalid project status: {value}. Allowed statuses: {', '.join([status for status in ProjectStatusEnum])}"
            )
        return value.lower()


class ProjectName(BaseVo):
    value: str

    @field_validator("value", mode="after")
    @classmethod
    def is_valid_name(cls, value: str) -> str:
        """
        :raises ProjectNameIsTooLongException:
        :raises EmptyStringException:
        """
        if not value:
            raise EmptyStringException("Project name cannot be empty.")
        if len(value) > CHAR_FIELD_MAX_LENGTH:
            raise ProjectNameIsTooLongException(
                f"Project name must be at most {CHAR_FIELD_MAX_LENGTH} characters long."
            )
        return value


class GoalSum(BaseVo):
    value: float

    @field_validator("value", mode="after")
    @classmethod
    def is_positive_goal_sum(cls, value: int) -> int:
        """:raises NegativeProjectGoalSumException:"""
        if value <= 0:
            raise NegativeProjectGoalSumException("goal_sum must be positive.")
        return value


class ProjectCreateCommand(BaseCommand):
    name: ProjectName
    description: Description
    category_id: Id
    creator_id: Id
    funding_model_id: Id
    stage: ProjectStage
    goal_sum: GoalSum
    deadline: DeadlineDate
    social_links: list[SocialLink]
    phone_number: PhoneNumber
    plan_file: PdfFile
    images: list[ImageFile]

    company_name: CompanyName
    country_code: CountryCode
    business_id: BusinessNumber
    established_date: EstablishedDate

    team_members: list[TeamMemberCreateCommand]
    company_founder: CompanyFounderCreateCommand


class ProjectUpdateCommand(BaseCommand):
    project_id: Id
    user_id: Id
    company: CompanyUpdatePayload | None
    name: ProjectName | None = None
    category_id: Id | None = None
    funding_model_id: Id | None = None
    stage: ProjectStage | None = None
    goal_sum: GoalSum | None = None
    deadline: DeadlineDate | None = None
    plan_file: PdfFile | None = None


class ProjectCreatePayload(AbstractCreatePayload, BaseVo):
    name: ProjectName
    description: Description
    category_id: Id
    creator_id: Id
    funding_model_id: Id
    stage: ProjectStage
    status: ProjectStatus
    goal_sum: GoalSum
    deadline: date
    plan_file: PdfFile


class ProjectUpdatePayload(AbstractUpdatePayload, BaseVo):
    id_: Id
    name: ProjectName | None = None
    category_id: Id | None = None
    funding_model_id: Id | None = None
    goal_sum: GoalSum | None = None
    stage: ProjectStage | None = None
    deadline: DeadlineDate | None = None
    plan_path: str | None = None


# ==== ProjectImage ====
class ProjectImageCreatePayload(AbstractCreatePayload, BaseVo):
    project_id: Id
    file_path: str
    order: int


class ProjectImageUpdatePayload(AbstractUpdatePayload, BaseVo):
    image_id: Id
    order: Order | None = None


class ProjectImageCreateCommand(BaseCommand):
    user_id: Id
    project_id: Id
    image_file: ImageFile


class ProjectImageUpdateCommand(BaseCommand):
    project_id: Id
    user_id: Id
    new_order: list[Order] | None = None


class ProjectImageDeletePayload(AbstractDeletePayload):
    project_id: Id
    image_order: int


class ProjectImageDeleteCommand(BaseCommand):
    project_id: Id
    image_order: int
    user_id: Id
