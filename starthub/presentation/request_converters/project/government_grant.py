from pprint import pformat
from typing import Any

from domain.value_objects.project.government_grant import (
    ProjectGovernmentGrantAmount,
    ProjectGovernmentGrantCreateCommand,
    ProjectGoverntmentGrantUpdateCommand,
    ProjectGrantName,
    ProjectGrantOrganizationName,
)
from loguru import logger
from presentation.request_converters.common import get_required_field
from rest_framework.request import Request


def request_to_project_government_grant_create_command(request: Request) -> ProjectGovernmentGrantCreateCommand:
    data: dict[str, Any] = request.data
    command = ProjectGovernmentGrantCreateCommand(
        grant_name=ProjectGrantName(value=get_required_field(data, "grant_name")),
        organization_name=ProjectGrantOrganizationName(value=get_required_field(data, "organization_name")),
        amount=ProjectGovernmentGrantAmount(value=get_required_field(data, "amount")),
    )
    logger.debug(f"commadn: \n{pformat(command.__dict__)}")
    return command


def request_to_project_government_grant_update_command(request: Request) -> ProjectGoverntmentGrantUpdateCommand:
    data: dict[str, Any] = request.data
    command = ProjectGoverntmentGrantUpdateCommand(
        grant_name=ProjectGrantName(value=data["grant_name"]) if "grant_name" in data else None,
        organization_name=(
            ProjectGrantOrganizationName(value=data["organization_name"]) if "organization_name" in data else None
        ),
        amount=ProjectGovernmentGrantAmount(value=data["amount"]) if "amount" in data else None,
    )
    logger.debug(f"commadn: \n{pformat(command.__dict__)}")
    return command
