from typing import Any

from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import QuerySet
from domain.enums.role import RoleEnum
from domain.models.role import Role
from domain.models.user_management.user import User
from loguru import logger


class Command(BaseCommand):
    """
    Django management command to assign default roles to users.

    This command finds all users who don't have any roles assigned
    and gives them the default role from RoleEnum.get_default().
    Uses atomic transaction to ensure data consistency.
    """

    help = "Assigns default role (user) for all users without any roles"

    def handle(self, *args: Any, **options: Any) -> None:
        logger.warning("Started.")
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
