from domain.enums.role import RoleEnum
from domain.value_objects.user_management.user_admin import UserAdminUpdateCommand
from loguru import logger
from rest_framework.request import Request


def request_to_user_admin_update_command(request: Request) -> UserAdminUpdateCommand:
    data = request.data
    command = UserAdminUpdateCommand(
        add_role=RoleEnum(value=data["add_role"]) if "add_role" in data else None,
        remove_role=RoleEnum(value=data["remove_role"]) if "remove_role" in data else None,
    )
    logger.info(f"command = {command}")
    return command
