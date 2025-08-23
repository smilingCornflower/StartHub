from typing import Any

from django.core.management.base import BaseCommand
from loguru import logger

from domain.enums.permission import ActionEnum, ScopeEnum
from domain.enums.role import RoleEnum
from domain.models.company import Company
from domain.models.permission import Permission
from domain.models.role import Role
from domain.services.permission import PermissionService
from domain.value_objects.user import PermissionVo


class Command(BaseCommand):
    help = "Create company permissions"

    def handle(self, *args: Any, **options: Any) -> None:
        logger.warning("Started.")

        self._assing_company_permissions()
        self._assing_business_id_permissions()

        logger.info("User permissions for company initialized")

    def _assing_company_permissions(self) -> None:
        for action in [ActionEnum.CHANGE, ActionEnum.DELETE]:
            permission_vo: PermissionVo = PermissionService.create_permission_vo(
                model=Company, action=action, scope=ScopeEnum.OWN
            )
            permission, _ = Permission.objects.get_or_create(name=permission_vo.value)

            user_role, _ = Role.objects.get_or_create(name=RoleEnum.USER)
            user_role.permissions.add(permission)

    def _assing_business_id_permissions(self) -> None:
        for action in [ActionEnum.CHANGE, ActionEnum.DELETE]:
            permission_vo: PermissionVo = PermissionService.create_permission_vo(
                model=Company,
                action=action,
                scope=ScopeEnum.OWN,
                field=Company.get_permission_key_for_business_id_field(),
            )
            permission, _ = Permission.objects.get_or_create(name=permission_vo.value)

            user_role, _ = Role.objects.get_or_create(name=RoleEnum.USER)
            user_role.permissions.add(permission)
