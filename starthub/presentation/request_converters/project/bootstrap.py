from rest_framework.request import Request

from domain.value_objects.common import Description
from domain.value_objects.project.bootstrap import ProjectBootstrapCreateCommand, ProjectBootstrapUpdateCommand
from presentation.request_converters.common import get_required_field


def request_to_project_bootstrap_create_command(request: Request) -> ProjectBootstrapCreateCommand:
    data = request.data
    return ProjectBootstrapCreateCommand(description=Description(value=get_required_field(data, "description")))


def request_to_project_bootstrap_update_command(request: Request) -> ProjectBootstrapUpdateCommand:
    data = request.data
    return ProjectBootstrapUpdateCommand(
        description=Description(value=data["description"]) if "description" in data else None,
    )
