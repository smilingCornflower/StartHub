from typing import Any

from django.core.management import call_command
from django.db import connection
from django.db.migrations.executor import MigrationExecutor
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from loguru import logger

_ran = False


@receiver(post_migrate)
def run_after_migrate(sender: Any, **kwargs: Any) -> None:
    global _ran
    if _ran:
        return

    logger.info("Applying commands...")

    executor = MigrationExecutor(connection)
    plan = executor.migration_plan(executor.loader.graph.leaf_nodes())

    if plan:
        return

    _ran = True
    call_command("assign_default_role_for_all_users_without_roles")
    call_command("create_blogger_role_and_permissions")
    call_command("create_company_permissions_for_users")
    call_command("create_kazakhstan_regions_and_cities")
    call_command("create_project_permissions_for_users")

    moderator_initialized, admin_initialized = False, False

    call_command("create_moderator_role_and_permissions")
    moderator_initialized = True

    if moderator_initialized:
        call_command("create_admin_role_and_permissions")
        admin_initialized = True

    if admin_initialized:
        call_command("create_super_admin_role_and_permissions")
