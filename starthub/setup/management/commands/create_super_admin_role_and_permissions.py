from typing import Any

from django.core.management.base import BaseCommand
from domain.enums.permission import ActionEnum, ScopeEnum
from domain.enums.role import RoleEnum
from domain.models.permission import Permission
from domain.models.role import Role
from domain.models.user_management.user import User
from domain.services.permission import PermissionService
from domain.value_objects.user_management.user import PermissionVo
from loguru import logger


class Command(BaseCommand):
    help = "Initialize superadmin role with required permissions for full system management"

    def handle(self, *args: Any, **options: Any) -> None:
        """
        Main command execution method for creating superadmin role.

        Creates superadmin role in the system with full permissions
        for complete system management and administration.
        """
        logger.warning("Initializing superadmin role and permissions...")
        super_admin = self._get_or_create_superadmin_role()

        self._copy_all_permissions_from_admin_role_to_super_admin(super_admin)
        self._setup_permissions_for_acting_with_user_roles(super_admin)

        logger.info("Superadmin role and permissions initialization completed")

    def _copy_all_permissions_from_admin_role_to_super_admin(self, super_admin_role: Role) -> None:
        admin_role = Role.objects.get(name=RoleEnum.ADMIN)
        for permission in admin_role.permissions.all():
            self._add_permission_to_role(super_admin_role, PermissionVo(value=permission.name))

    def _setup_permissions_for_acting_with_user_roles(self, super_admin_role: Role) -> None:
        add_admin_role_to_any_user = PermissionService.create_permission_vo(
            model=User, action=ActionEnum.ADD, scope=ScopeEnum.ANY, field=User.ROLES_FIELD, value=RoleEnum.ADMIN
        )
        remove_admin_role_from_any_user = PermissionService.create_permission_vo(
            model=User, action=ActionEnum.DELETE, scope=ScopeEnum.ANY, field=User.ROLES_FIELD, value=RoleEnum.ADMIN
        )

        self._add_permission_to_role(role=super_admin_role, permission_vo=add_admin_role_to_any_user)
        self._add_permission_to_role(role=super_admin_role, permission_vo=remove_admin_role_from_any_user)

    def _get_or_create_superadmin_role(self) -> Role:
        """
        Creates or retrieves existing superadmin role.
        """
        role, created = Role.objects.get_or_create(name=RoleEnum.SUPER_ADMIN)
        if created:
            logger.info("Created new superadmin role")
        return role

    def _add_permission_to_role(self, role: Role, permission_vo: PermissionVo) -> None:
        permission, _ = Permission.objects.get_or_create(name=permission_vo.value)

        if not role.permissions.filter(id=permission.id).exists():
            role.permissions.add(permission)
            logger.debug(f"Added permission '{permission.name}' to superadmin role '{role.name}'")
