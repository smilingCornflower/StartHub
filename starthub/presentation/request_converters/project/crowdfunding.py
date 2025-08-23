from typing import Any

from loguru import logger
from rest_framework.request import Request

from domain.value_objects.project.crowdfunding import (
    ProjectCrowdfundingAmount,
    ProjectCrowdfundingCreateCommand,
    ProjectCrowdfundingName,
    ProjectCrowdfundingUpdateCommand,
)
from presentation.request_converters.common import get_required_field


def request_to_project_crowdfunding_create_command(request: Request) -> ProjectCrowdfundingCreateCommand:
    data: dict[str, Any] = request.data

    command = ProjectCrowdfundingCreateCommand(
        name=ProjectCrowdfundingName(value=get_required_field(data, "name")),
        amount=ProjectCrowdfundingAmount(value=get_required_field(data, "amount")),
    )
    logger.debug(f"command = {command}")
    return command


def request_to_project_crowdfunding_update_command(request: Request) -> ProjectCrowdfundingUpdateCommand:
    data: dict[str, Any] = request.data

    command = ProjectCrowdfundingUpdateCommand(
        name=ProjectCrowdfundingName(value=data["name"]) if "name" in data else None,
        amount=ProjectCrowdfundingAmount(value=data["amount"]) if "amount" in data else None,
    )
    logger.debug(f"command = {command}")
    return command
