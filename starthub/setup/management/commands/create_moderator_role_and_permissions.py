from typing import Any

from django.core.management.base import BaseCommand
from domain.enums.permission import ActionEnum, ScopeEnum
from domain.enums.project_status import ProjectStatusEnum
from domain.enums.role import RoleEnum
from domain.models.permission import Permission
from domain.models.project_management.project import Project
from domain.models.role import Role
from domain.services.permission import PermissionService
from domain.value_objects.user_management.user import PermissionVo
from loguru import logger


class Command(BaseCommand):
    help = "Initialize moderator role with required permissions for project management"

    def handle(self, *args: Any, **options: Any) -> None:
        """
        Main command execution method for creating moderator role.

        Creates moderator role in the system with basic permissions
        for project and user management.
        """
        logger.warning("Initializing moderator role and permissions...")

        moderator_role = self._get_or_create_moderator_role()

        self._setup_permissions_for_special_status_projects(moderator_role)

        logger.info("Moderator role and permissions initialization completed")

    def _get_or_create_moderator_role(self) -> Role:
        """
        Creates or retrieves existing moderator role.
        """
        role, created = Role.objects.get_or_create(name=RoleEnum.MODERATOR)
        if created:
            logger.info("Created new moderator role")
        return role

    def _add_permission_to_role(self, role: Role, permission_vo: PermissionVo) -> None:
        permission, _ = Permission.objects.get_or_create(name=permission_vo.value)

        if not role.permissions.filter(id=permission.id).exists():
            role.permissions.add(permission)
            logger.debug(f"Added permission '{permission.name}' to moderator role '{role.name}'")

    def _setup_permissions_for_special_status_projects(self, role: Role) -> None:
        """Setup project submission permissions for admin role."""
        view_any_project_under_moderation = PermissionService.create_permission_vo(
            model=Project,
            action=ActionEnum.VIEW,
            scope=ScopeEnum.ANY,
            field=Project.STATUS_FIELD,
            value=ProjectStatusEnum.UNDER_MODERATION,
        )
        change_any_project_under_moderation = PermissionService.create_permission_vo(
            model=Project,
            action=ActionEnum.CHANGE,
            scope=ScopeEnum.ANY,
            field=Project.STATUS_FIELD,
            value=ProjectStatusEnum.UNDER_MODERATION,
        )

        self._add_permission_to_role(role, view_any_project_under_moderation)
        self._add_permission_to_role(role, change_any_project_under_moderation)

        logger.info("Project permissions configured")
