import json
from typing import Any

from config.settings import BASE_DIR
from django.core.management.base import BaseCommand
from domain.models.geo.city import City
from domain.models.geo.country import Country
from domain.models.geo.region import Region
from loguru import logger


class Command(BaseCommand):
    help = "Ensure all cities and regions of Kazakhstan exist."

    def handle(self, *args: Any, **options: Any) -> None:
        logger.warning("Started command: create_blogger_role_and_permissions")
        file_path = BASE_DIR / "../fixtures/kazakhstan_cities_by_region.json"

        with file_path.open(encoding="utf-8") as f:
            data = json.load(f)

        country, _ = Country.objects.get_or_create(code="KZ")

        for region_name, city_names in data.items():
            region, _ = Region.objects.get_or_create(name=region_name, country=country)
            for city_name in city_names:
                City.objects.get_or_create(name=city_name, region=region)

        logger.info("All cities and regions for Kazakhstan have been created or already existed.")
