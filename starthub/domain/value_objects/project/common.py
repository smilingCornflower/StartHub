from domain.constants import CHAR_FIELD_MAX_LENGTH
from domain.enums.project_stage import ProjectStageEnum
from domain.enums.project_status import ProjectStatusEnum
from domain.exceptions.project_management import (
    InvalidProjectStageException,
    InvalidProjectStatusException,
    NegativeProjectGoalSumException,
    ProjectNameIsTooLongException,
)
from domain.value_objects import BaseVo
from domain.value_objects.common import StringVo
from pydantic import field_validator


class ProjectStageVo(BaseVo):
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


class ProjectName(StringVo):
    max_length = CHAR_FIELD_MAX_LENGTH
    too_long_string_exception = ProjectNameIsTooLongException

    @classmethod
    def get_empty_string_msg(cls) -> str:
        return "Project name cannot be empty."

    @classmethod
    def get_too_long_string_msg(cls) -> str:
        return f"Project name must be at most {cls.max_length} characters long."


class GoalSum(BaseVo):
    value: float

    @field_validator("value", mode="after")
    @classmethod
    def is_positive_goal_sum(cls, value: int) -> int:
        """:raises NegativeProjectGoalSumException:"""
        if value <= 0:
            raise NegativeProjectGoalSumException("goal_sum must be positive.")
        return value
