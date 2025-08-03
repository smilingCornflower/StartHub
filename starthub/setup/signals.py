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
    call_command("assign_default_role")
    call_command("assing_project_permissions_for_user")
    call_command("create_blogger_role_and_permissions")
