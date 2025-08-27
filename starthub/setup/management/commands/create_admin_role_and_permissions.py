from typing import Any

from django.core.management.base import BaseCommand
from domain.enums.permission import ActionEnum, ScopeEnum
from domain.enums.role import RoleEnum
from domain.models import FundingModel
from domain.models.permission import Permission
from domain.models.project_management.project import Project
from domain.models.role import Role
from domain.models.user_management.message import UserMessage
from domain.models.user_management.user import User
from domain.services.permission import PermissionService
from domain.value_objects.user_management.user import PermissionVo
from loguru import logger


class Command(BaseCommand):
    """
    Django management command to initialize admin role and permissions.

    Creates the ADMIN role if it doesn't exist and assigns necessary permissions
    for managing projects and project submissions. This command is idempotent
    and can be run multiple times safely.
    """

    help = "Initialize admin role with required permissions for project management"

    def handle(self, *args: Any, **options: Any) -> None:
        logger.warning("Initializing admin role and permissions...")

        admin_role = self._get_or_create_admin_role()

        self._copy_all_permissions_from_moderator_role_to_admin()
        self._setup_project_permissions(admin_role)
        self._setup_permissions_for_user_roles(admin_role)
        self._setup_permissions_for_user_is_active_field(admin_role)
        self._setup_permission_to_view_any_user_messages(admin_role)
        self._add_view_any_user_details_permission(admin_role)
        self._add_view_any_permissions_permisssion(admin_role)
        self._add_change_any_funding_model_permission(admin_role)

        logger.info("Admin role and permissions initialization completed")

    def _add_permission_to_role(self, role: Role, permission_vo: PermissionVo) -> None:
        """Add permission to role if it doesn't already exist."""
        permission, _ = Permission.objects.get_or_create(name=permission_vo.value)

        if not role.permissions.filter(id=permission.id).exists():
            role.permissions.add(permission)
            logger.debug(f"Added permission '{permission.name}' to role '{role.name}'")

    def _get_or_create_admin_role(self) -> Role:
        """Get or create the admin role."""
        role, created = Role.objects.get_or_create(name=RoleEnum.ADMIN)
        if created:
            logger.info("Created new admin role")
        return role

    def _copy_all_permissions_from_moderator_role_to_admin(self) -> None:
        admin_role = self._get_or_create_admin_role()
        moderator_role = Role.objects.get(name=RoleEnum.MODERATOR)
        for permission in moderator_role.permissions.all():
            self._add_permission_to_role(admin_role, PermissionVo(value=permission.name))
        logger.info("All permissions from moderator copied to admin.")

    def _add_view_any_user_details_permission(self, role: Role) -> None:
        view_any_user_details = PermissionService.create_permission_vo(
            model=User,
            action=ActionEnum.VIEW,
            scope=ScopeEnum.ANY,
            field=User.DETAILS_FIED,
        )
        self._add_permission_to_role(role, view_any_user_details)

    def _add_change_any_funding_model_permission(self, role: Role) -> None:
        change_any_funding_model_permission = PermissionService.create_permission_vo(
            model=FundingModel, action=ActionEnum.CHANGE, scope=ScopeEnum.ANY
        )
        self._add_permission_to_role(role, change_any_funding_model_permission)

    def _add_view_any_permissions_permisssion(self, role: Role) -> None:
        view_any_permissions_permission = PermissionService.create_permission_vo(
            model=Permission, action=ActionEnum.VIEW, scope=ScopeEnum.ANY
        )
        self._add_permission_to_role(role, view_any_permissions_permission)

    def _setup_project_permissions(self, admin_role: Role) -> None:
        """Setup project-related permissions for admin role."""
        change_any_project_status = PermissionService.create_permission_vo(
            model=Project, action=ActionEnum.CHANGE, scope=ScopeEnum.ANY, field=Project.STATUS_FIELD
        )

        self._add_permission_to_role(admin_role, change_any_project_status)
        logger.info("Project permissions configured")

    def _setup_permissions_for_user_is_active_field(self, admin_role: Role) -> None:
        change_any_user_is_active_field = PermissionService.create_permission_vo(
            model=User,
            action=ActionEnum.CHANGE,
            scope=ScopeEnum.ANY,
            field=User.IS_ACTIVE_FIELD,
        )
        self._add_permission_to_role(admin_role, change_any_user_is_active_field)

    def _setup_permission_to_view_any_user_messages(self, admin_role: Role) -> None:
        view_any_message = PermissionService.create_permission_vo(
            model=UserMessage, action=ActionEnum.VIEW, scope=ScopeEnum.ANY
        )
        self._add_permission_to_role(role=admin_role, permission_vo=view_any_message)

    def _setup_permissions_for_user_roles(self, admin_role: Role) -> None:
        add_moderator_to_any_user = PermissionService.create_permission_vo(
            model=User, action=ActionEnum.ADD, scope=ScopeEnum.ANY, field=User.ROLES_FIELD, value=RoleEnum.MODERATOR
        )
        add_blogger_to_any_user = PermissionService.create_permission_vo(
            model=User, action=ActionEnum.ADD, scope=ScopeEnum.ANY, field=User.ROLES_FIELD, value=RoleEnum.BLOGGER
        )
        remove_moderator_from_any_user = PermissionService.create_permission_vo(
            model=User, action=ActionEnum.DELETE, scope=ScopeEnum.ANY, field=User.ROLES_FIELD, value=RoleEnum.MODERATOR
        )
        remove_blogger_from_any_user = PermissionService.create_permission_vo(
            model=User, action=ActionEnum.DELETE, scope=ScopeEnum.ANY, field=User.ROLES_FIELD, value=RoleEnum.BLOGGER
        )
        self._add_permission_to_role(role=admin_role, permission_vo=add_moderator_to_any_user)
        self._add_permission_to_role(role=admin_role, permission_vo=add_blogger_to_any_user)
        self._add_permission_to_role(role=admin_role, permission_vo=remove_moderator_from_any_user)
        self._add_permission_to_role(role=admin_role, permission_vo=remove_blogger_from_any_user)
