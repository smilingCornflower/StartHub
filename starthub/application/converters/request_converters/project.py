from datetime import date
from typing import Any, cast

import pydantic
from django.http import QueryDict
from domain.exceptions.validation import DateIsNotIsoFormatException, ValidationException
from domain.value_objects.common import FirstName, Id, LastName, PhoneNumber, Slug, SocialLink
from domain.value_objects.filter import ProjectFilter
from domain.value_objects.project_management import (
    ProjectCreatePayload,
    ProjectUpdatePayload,
    TeamMemberInProjectCreatePayload,
)
from loguru import logger


def request_data_to_project_filter(data: QueryDict) -> ProjectFilter:
    filter_ = ProjectFilter()

    if data.get("category_slug"):
        filter_.category_slug = Slug(value=cast(str, data.get("category_slug")))
    if data.get("funding_model_slug"):
        filter_.funding_model_slug = Slug(value=cast(str, data.get("funding_model_slug")))

    return filter_


def request_data_to_project_create_payload(data: dict[str, Any], user_id: int) -> ProjectCreatePayload:
    """
    :raises ValueError: if invalid data format or missing required fields.
    :raises ValidationException: if business rules was violated.
    """
    try:
        team_members: list[TeamMemberInProjectCreatePayload] = []
        for member in data["team_members"]:
            team_members.append(
                TeamMemberInProjectCreatePayload(
                    first_name=FirstName(value=member["first_name"]),
                    last_name=LastName(value=member["last_name"]),
                    description=member["description"],
                )
            )
        try:
            deadline = date.fromisoformat(data["deadline"])
        except ValueError:
            raise DateIsNotIsoFormatException("Date must be in iso format.")

        return ProjectCreatePayload(
            name=data["name"],
            description=data["description"],
            category_id=Id(value=data["category_id"]),
            creator_id=Id(value=user_id),
            funding_model_id=Id(value=data["funding_model_id"]),
            goal_sum=data["goal_sum"],
            team_members=team_members,
            deadline=deadline,
            company_id=Id(value=data["company_id"]),
            social_links=[SocialLink(platform=k, link=v) for k, v in data["social_links"].items()],
            phone_number=PhoneNumber(value=data["phone_number"]),
        )
    except KeyError as e:
        logger.error(e)
        raise KeyError("Missing required field.")
    except (pydantic.ValidationError, ValueError) as e:
        logger.error(e)
        raise ValueError(str(e))
    except ValidationException as e:
        logger.error(e)
        raise


def request_data_to_project_update_payload(request_data: dict[str, Any], project_id: int) -> ProjectUpdatePayload:
    """
    :raises KeyError:
    :raises ValueError:
    :raises ValidationException:
    """
    deadline = None
    if request_data.get("deadline"):
        try:
            deadline = date.fromisoformat(request_data["deadline"])
        except (TypeError, ValueError):
            raise ValueError("deadline must be string in ISO format date.")

    try:
        return ProjectUpdatePayload(
            id_=Id(value=project_id),
            name=request_data.get("name"),
            description=request_data.get("description"),
            category_id=(
                Id(value=cast(Any, request_data.get("category_id"))) if request_data.get("category_id") else None
            ),
            funding_model_id=(
                Id(value=cast(Any, request_data.get("funding_model_id")))
                if request_data.get("funding_model_id")
                else None
            ),
            goal_sum=request_data.get("goal_sum"),
            deadline=deadline,
        )
    except KeyError as e:
        logger.error(e)
        raise ValueError("Missing required field.")
    except ValidationException as e:
        logger.error(e)
        raise
    except pydantic.ValidationError as e:
        logger.error(f"ValidationError: {e}")
        raise ValueError("Invalid data format.")
