from typing import Any

from django.core.management import call_command
from django.db.models.signals import post_migrate
from django.dispatch import receiver


@receiver(post_migrate)
def run_after_migrate(sender: Any, **kwargs: Any) -> None:
    call_command("assign_default_role")
    call_command("create_blogger_role")
