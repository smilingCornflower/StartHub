from domain.value_objects.project.useful_link import UsefulLinkCreateCommand, UsefulLinkName
from loguru import logger
from presentation.request_converters.common import get_required_field
from rest_framework.request import Request


def request_to_useful_link_create_command(request: Request) -> UsefulLinkCreateCommand:
    data = request.data
    command = UsefulLinkCreateCommand(
        name=UsefulLinkName(value=get_required_field(data, "name")),
        url=get_required_field(data, "url"),
    )
    logger.debug(f"command = {command}")
    return command
