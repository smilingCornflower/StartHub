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
from domain.value_objects import BaseVo
from pydantic import field_validator


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
