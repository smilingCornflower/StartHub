from domain.enums.role import RoleEnum
from domain.exceptions.validation import ValidationException
from domain.value_objects.user_management.user_admin import UserAdminUpdateCommand
from loguru import logger
from rest_framework.request import Request


def request_to_user_admin_update_command(request: Request) -> UserAdminUpdateCommand:
    """:raises ValidationException: if role appears to be invalid"""
    data = request.data

    add_role = data.get("add_role")
    if add_role and add_role not in RoleEnum:
        raise ValidationException(f"Invalid role '{add_role}'. Allowed roles: {', '.join([i for i in RoleEnum])}")

    remove_role = data.get("remove_role")
    if remove_role and remove_role not in RoleEnum:
        raise ValidationException(f"Invalid role '{remove_role}'. Allowed roles: {', '.join([i for i in RoleEnum])}")

    command = UserAdminUpdateCommand(
        add_role=RoleEnum(value=add_role) if add_role else None,
        remove_role=RoleEnum(value=remove_role) if remove_role else None,
    )
    logger.info(f"command = {command}")
    return command
