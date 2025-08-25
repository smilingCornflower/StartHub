from typing import Any

from django.core.management.base import BaseCommand
from domain.enums.permission import ActionEnum, ScopeEnum
from domain.enums.role import RoleEnum
from domain.models.news import News
from domain.models.permission import Permission
from domain.models.role import Role
from domain.services.permission import PermissionService
from domain.value_objects.user_management.user import PermissionVo
from loguru import logger


class Command(BaseCommand):
    """
    Django management command to create blogger role and assign news permissions.

    Creates the BLOGGER role and assigns ADD, CHANGE, and DELETE permissions
    for the News model with ANY scope. This allows bloggers to manage
    all news articles in the system.
    """

    help = "Ensure 'blogger' role and permissions exist"

    def handle(self, *args: Any, **options: Any) -> None:
        logger.warning("Started ensuring blogger role and permissions.")

        blogger, _ = Role.objects.get_or_create(name=RoleEnum.BLOGGER)

        # Base roles for blogger
        for action in [ActionEnum.ADD, ActionEnum.CHANGE, ActionEnum.DELETE]:
            manage_news_permission: PermissionVo = PermissionService.create_permission_vo(
                model=News, action=action, scope=ScopeEnum.ANY
            )
            permission, _ = Permission.objects.get_or_create(name=manage_news_permission.value)
            if permission not in blogger.permissions.all():
                blogger.permissions.add(permission)
                logger.debug(f"Permission {permission.name} added to blogger role.")

        self._setup_permission_for_news_is_active_field(blogger_role=blogger)

    def _setup_permission_for_news_is_active_field(self, blogger_role: Role) -> None:
        change_news_is_active_field_permission = PermissionService.create_permission_vo(
            model=News,
            action=ActionEnum.CHANGE,
            scope=ScopeEnum.ANY,
            field=News.IS_ACTIVE_FIELD,
        )
        permission, created = Permission.objects.get_or_create(name=change_news_is_active_field_permission.value)
        if permission not in blogger_role.permissions.all():
            blogger_role.permissions.add(permission)
            logger.debug(f"Permission {permission.name} added to blogger role.")

        logger.info("Blogger permissions initialized")
