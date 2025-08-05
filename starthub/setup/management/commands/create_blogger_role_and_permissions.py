from typing import Any

from django.core.management.base import BaseCommand
from domain.enums.permission import ActionEnum, ScopeEnum
from domain.enums.role import RoleEnum
from domain.models.news import News
from domain.models.permission import Permission
from domain.models.role import Role
from domain.services.permission import PermissionService
from domain.value_objects.user import PermissionVo
from loguru import logger


class Command(BaseCommand):
    help = "Ensure 'blogger' role and permissions exist"

    def handle(self, *args: Any, **options: Any) -> None:
        logger.warning("Started command: create_blogger_role_and_permissions")
        for action in [ActionEnum.ADD, ActionEnum.CHANGE, ActionEnum.DELETE]:
            manage_news_permission: PermissionVo = PermissionService.create_permission_vo(
                model=News, action=action, scope=ScopeEnum.ANY
            )

            permission, _ = Permission.objects.get_or_create(name=manage_news_permission.value)
            role, _ = Role.objects.get_or_create(name=RoleEnum.BLOGGER)
            role.permissions.add(permission)

        logger.info("Blogger permissions initialized")
