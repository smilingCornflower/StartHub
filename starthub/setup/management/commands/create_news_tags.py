from typing import Any

from django.core.management.base import BaseCommand
from domain.enums.news_tag import NewsTagEnum
from domain.models.news_management.news_tag import NewsTag


class Command(BaseCommand):
    help = "Ensure all tags exist."

    def handle(self, *args: Any, **options: Any) -> None:
        for tag_name in NewsTagEnum:
            NewsTag.objects.get_or_create(name=tag_name)
