from domain.value_objects.common import Description
from domain.value_objects.project.stage import ProjectStageUpdateCommand
from loguru import logger
from rest_framework.request import Request


def request_to_project_stage_update_command(request: Request) -> ProjectStageUpdateCommand:
    data = request.data
    command = ProjectStageUpdateCommand(
        description=Description(value=data["description"]) if "description" in data else None,
    )
    logger.debug(f"command = {command}")
    return command
