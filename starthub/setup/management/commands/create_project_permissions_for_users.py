from typing import Any

from django.core.management.base import BaseCommand
from domain.enums.permission import ActionEnum, ScopeEnum
from domain.enums.role import RoleEnum
from domain.models import ProjectIncubator
from domain.models.permission import Permission
from domain.models.project_management.accelerator import ProjectAccelerator
from domain.models.project_management.project import Project
from domain.models.role import Role
from domain.services.permission import PermissionService
from domain.value_objects.user import PermissionVo
from loguru import logger


class Command(BaseCommand):
    help = "Assigns project permissions for user"

    def handle(self, *args: Any, **options: Any) -> None:
        self.assing_project_permissions_for_users()
        self._assign_project_accelerator_permission_for_users()
        self._assign_project_incubator_permission_for_users()

    def assing_project_permissions_for_users(self) -> None:
        logger.warning("Started command: assing_project_permissions_for_users()")
        for action in [ActionEnum.CHANGE, ActionEnum.DELETE]:
            permission_vo: PermissionVo = PermissionService.create_permission_vo(
                model=Project, action=action, scope=ScopeEnum.OWN
            )
            permission, _ = Permission.objects.get_or_create(name=permission_vo.value)

            user_role, _ = Role.objects.get_or_create(name=RoleEnum.USER)
            user_role.permissions.add(permission)

        logger.info("User permissions for project initialized")

    def _assign_project_accelerator_permission_for_users(self) -> None:
        logger.warning("Started command: _assign_project_accelerator_permission_for_users()")

        for action in [ActionEnum.ADD, ActionEnum.CHANGE, ActionEnum.DELETE]:
            permission_vo: PermissionVo = PermissionService.create_permission_vo(
                model=ProjectAccelerator, action=action, scope=ScopeEnum.OWN
            )
            permission, _ = Permission.objects.get_or_create(name=permission_vo.value)

            user_role, _ = Role.objects.get_or_create(name=RoleEnum.USER)
            user_role.permissions.add(permission)

        logger.info("User permissions for project accelerator initialized")

    def _assign_project_incubator_permission_for_users(self) -> None:
        logger.warning("Started _assign_project_incubator_permission_for_users()")

        for action in [ActionEnum.ADD, ActionEnum.CHANGE, ActionEnum.DELETE]:
            permission_vo: PermissionVo = PermissionService.create_permission_vo(
                model=ProjectIncubator, action=action, scope=ScopeEnum.OWN
            )
            permission, _ = Permission.objects.get_or_create(name=permission_vo.value)

            user_role, _ = Role.objects.get_or_create(name=RoleEnum.USER)
            user_role.permissions.add(permission)

        logger.info("User permissions for project incubator initialized")
