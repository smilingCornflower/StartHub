from domain.enums.role import RoleEnum
from domain.value_objects.project.submission import ProjectRejectCommand, ProjectRejectReport
from domain.value_objects.user_management.admin import UserAdminUpdateCommand
from loguru import logger
from presentation.request_converters.common import get_required_field
from rest_framework.request import Request


def request_to_user_admin_update_command(request: Request) -> UserAdminUpdateCommand:
    data = request.data
    command = UserAdminUpdateCommand(
        add_role=RoleEnum(value=data["add_role"]) if "add_role" in data else None,
        remove_role=RoleEnum(value=data["remove_role"]) if "remove_role" in data else None,
    )
    logger.info(f"command = {command}")
    return command


def request_to_project_submission_reject_command(request: Request) -> ProjectRejectCommand:
    data = request.data
    return ProjectRejectCommand(report=ProjectRejectReport(value=get_required_field(data, "report")))
