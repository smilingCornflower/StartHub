from typing import Any

from django.core.management.base import BaseCommand
from loguru import logger

from domain.enums.permission import ActionEnum, ScopeEnum
from domain.enums.role import RoleEnum
from domain.models.news import News
from domain.models.permission import Permission
from domain.models.role import Role
from domain.services.permission import PermissionService
from domain.value_objects.user import PermissionVo


class Command(BaseCommand):
    help = "Ensure 'blogger' role with 'manage.any.news' permission exists"

    def handle(self, *args: Any, **options: Any) -> None:
        for action in [ActionEnum.ADD, ActionEnum.CHANGE, ActionEnum.DELETE]:
            manage_news_permission: PermissionVo = PermissionService.create_permission_vo(
                model=News, action=action, scope=ScopeEnum.ANY
            )

            permission, _ = Permission.objects.get_or_create(name=manage_news_permission.value)
            role, _ = Role.objects.get_or_create(name=RoleEnum.BLOGGER)
            role.permissions.add(permission)