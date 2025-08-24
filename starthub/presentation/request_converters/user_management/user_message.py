from domain.value_objects.common import FirstName, LastName, PhoneNumber
from domain.value_objects.user_management.user import Email
from domain.value_objects.user_management.user_message import (
    UserMessageContent,
    UserMessageCreateCommand,
    UserMessageTopic,
)
from loguru import logger
from presentation.request_converters.common import get_required_field
from rest_framework.request import Request


def request_to_user_message_create_command(request: Request) -> UserMessageCreateCommand:
    data = request.data
    command = UserMessageCreateCommand(
        first_name=FirstName(value=get_required_field(data, "first_name")),
        last_name=LastName(value=get_required_field(data, "last_name")),
        email=Email(value=get_required_field(data, "email")),
        phone=PhoneNumber(value=get_required_field(data, "phone")),
        topic=UserMessageTopic(value=get_required_field(data, "topic")),
        content=UserMessageContent(value=get_required_field(data, "content")),
    )
    logger.debug(f"command = {command}")
    return command
