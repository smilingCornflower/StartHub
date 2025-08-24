from typing import cast

from django.http import QueryDict
from domain.exceptions.validation import ValidationException
from domain.value_objects.common import FirstName, LastName, PhoneNumber
from domain.value_objects.user_management.user import Email
from domain.value_objects.user_management.user_message import (
    UserMessageContent,
    UserMessageCreateCommand,
    UserMessageGetCommand,
    UserMessageOrderByEnum,
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


def request_to_user_message_get_command(request: Request) -> UserMessageGetCommand:
    params: QueryDict = request.query_params

    is_read_param = params.get("is_read")
    if is_read_param is None:
        is_read = None
    elif is_read_param == "true":
        is_read = True
    elif is_read_param == "false":
        is_read = False
    else:
        raise ValidationException(f"Invalid value for is_read: {is_read_param}. Expected 'true' or 'false'")

    try:
        order_by = UserMessageOrderByEnum(value=cast(str, params["order_by"])) if "order_by" in params else None
    except ValueError:
        allowed = ", ".join([item for item in UserMessageOrderByEnum])
        raise ValidationException(f"Invalid value for order_by: {params['order_by']}. Expected: {allowed}")

    command = UserMessageGetCommand(
        is_read=is_read,
        order_by=order_by,
    )
    logger.debug(f"command = {command}")
    return command
