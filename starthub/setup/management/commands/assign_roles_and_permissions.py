from typing import Any

from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import QuerySet
from domain.enums.permission import ActionEnum, ScopeEnum
from domain.enums.role import RoleEnum
from domain.models.company import Company
from domain.models.news import News
from domain.models.permission import Permission
from domain.models.role import Role
from domain.models.user import User
from domain.services.permission import PermissionService
from domain.value_objects.user import PermissionVo
from loguru import logger


class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> None:
        self.assign_default_role()
        self.create_blogger_role_and_permissions()
        self.assing_company_permission_for_users()

    def assign_default_role(self) -> None:
        logger.warning("Started command: assing_default_role")
        logger.info("Checking users without any roles...")

        user_role, _ = Role.objects.get_or_create(name=RoleEnum.get_default())

        users_without_any_roles: QuerySet[User] = User.objects.filter(roles__isnull=True)
        count: int = users_without_any_roles.count()

        if not count:
            logger.info("All users have roles")
            return

        with transaction.atomic():
            for user in users_without_any_roles:
                user.roles.add(user_role)

        logger.info("Roles are assigned")

    def create_blogger_role_and_permissions(self) -> None:
        logger.warning("Started command: create_blogger_role_and_permissions")
        for action in [ActionEnum.ADD, ActionEnum.CHANGE, ActionEnum.DELETE]:
            manage_news_permission: PermissionVo = PermissionService.create_permission_vo(
                model=News, action=action, scope=ScopeEnum.ANY
            )

            permission, _ = Permission.objects.get_or_create(name=manage_news_permission.value)
            role, _ = Role.objects.get_or_create(name=RoleEnum.BLOGGER)
            role.permissions.add(permission)

        logger.info("Blogger permissions initialized")

    def assing_company_permission_for_users(self, *args: Any, **options: Any) -> None:
        logger.warning("Started command: assing_company_permissions_for_users")

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
