from typing import Any

from domain.value_objects.project.government_grant import (
    ProjectGovernmentGrantAmount,
    ProjectGoverntmentGrantCreateCommand,
    ProjectGrantName,
    ProjectGrantOrganizationName,
)
from presentation.request_converters.common import get_required_field
from rest_framework.request import Request


def request_to_project_government_grant_create_command(request: Request) -> ProjectGoverntmentGrantCreateCommand:
    data: dict[str, Any] = request.data
    return ProjectGoverntmentGrantCreateCommand(
        grant_name=ProjectGrantName(value=get_required_field(data, "grant_name")),
        organization_name=ProjectGrantOrganizationName(value=get_required_field(data, "organization_name")),
        amount=ProjectGovernmentGrantAmount(value=get_required_field(data, "amount")),
    )
