from typing import Any

from django.core.management.base import BaseCommand
from domain.enums.permission import ActionEnum, ScopeEnum
from domain.enums.role import RoleEnum
from domain.models.permission import Permission
from domain.models.project_management.project import Project
from domain.models.role import Role
from domain.services.permission import PermissionService
from loguru import logger


class Command(BaseCommand):
    """
    Django management command to create admin role and assign permissions.

    Creates the ADMIN role and assigns specified permissions to it.
    This allows administrators to manage system resources.
    """

    help = "Create admin role and permissions"

    def handle(self, *args: Any, **options: Any) -> None:
        logger.warning("Started.")

        role, _ = Role.objects.get_or_create(name=RoleEnum.ADMIN)
        change_any_project_status_permission = PermissionService.create_permission_vo(
            model=Project, action=ActionEnum.CHANGE, scope=ScopeEnum.ANY, field=Project.STATUS_FIELD
        )
        permission, _ = Permission.objects.get_or_create(name=change_any_project_status_permission.value)
        role.permissions.add(permission)

        logger.info("Admin permissions initialized")
