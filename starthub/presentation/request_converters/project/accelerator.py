from typing import Any

from domain.value_objects.common import Description
from domain.value_objects.project.accelerator import (
    AcceleratorName,
    ProjectAcceleratorCreateCommand,
    ProjectAcceleratorUpdateCommand,
)
from loguru import logger
from presentation.request_converters.common import get_required_field
from rest_framework.request import Request


def request_to_project_accelerator_create_command(request: Request) -> ProjectAcceleratorCreateCommand:
    data: dict[str, Any] = request.data
    command = ProjectAcceleratorCreateCommand(
        name=AcceleratorName(value=get_required_field(data, "name")),
        description=Description(value=get_required_field(data, "description")),
    )
    logger.debug(f"command = {command}")
    return command


def request_to_project_accelerator_update_command(request: Request) -> ProjectAcceleratorUpdateCommand:
    data: dict[str, Any] = request.data
    command = ProjectAcceleratorUpdateCommand(
        name=AcceleratorName(value=data["name"]) if "name" in data else None,
        description=Description(value=data["description"]) if "description" in data else None,
    )
    logger.debug(f"command = {command}")
    return command
