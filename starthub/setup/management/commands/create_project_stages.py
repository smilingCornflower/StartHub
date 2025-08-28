from typing import Any

from django.core.management.base import BaseCommand
from domain.enums.project_stage import ProjectStageEnum
from domain.models.project_management.project_stage import ProjectStage
from loguru import logger


class Command(BaseCommand):
    help = "create all project steps from ProjectStepEnum"

    def handle(self, *args: Any, **options: Any) -> None:
        for stage in ProjectStageEnum:
            ProjectStage.objects.get_or_create(name=stage)
        logger.info("All project stages created.")
