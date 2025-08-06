from typing import Any

from django.core.management.base import BaseCommand
from domain.enums.permission import ActionEnum, ScopeEnum
from domain.enums.role import RoleEnum
from domain.models.permission import Permission
from domain.models.project_management.project import Project
from domain.models.role import Role
from domain.services.permission import PermissionService
from domain.value_objects.user import PermissionVo
from loguru import logger


class Command(BaseCommand):
    help = "Assigns project permissions for user"

    def handle(self, *args: Any, **options: Any) -> None:
        logger.warning("Started command: assing_project_permissions_for_users")
        for action in [ActionEnum.CHANGE, ActionEnum.DELETE]:
            permission_vo: PermissionVo = PermissionService.create_permission_vo(
                model=Project, action=action, scope=ScopeEnum.OWN
            )
            permission, _ = Permission.objects.get_or_create(name=permission_vo.value)

            user_role, _ = Role.objects.get_or_create(name=RoleEnum.USER)
            user_role.permissions.add(permission)

        logger.info("User permissions for project initialized")
