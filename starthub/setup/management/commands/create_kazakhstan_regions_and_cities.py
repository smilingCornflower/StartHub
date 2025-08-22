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
        logger.warning("Started.")

        file_path = BASE_DIR / "../fixtures/kazakhstan_cities_by_region.json"

        with file_path.open(encoding="utf-8") as f:
            data = json.load(f)

        country, _ = Country.objects.get_or_create(code="KZ")

        for region_kk, region_ru, region_en in zip(data["kz"], data["ru"], data["en"]):
            region, _ = Region.objects.get_or_create(name_en=region_en, country=country)
            if region.name_kk != region_kk or region.name_ru != region_ru:  # type: ignore[attr-defined]
                region.name_kk = region_kk  # type: ignore[attr-defined]
                region.name_ru = region_ru  # type: ignore[attr-defined]
                region.save()

            for city_kz, city_ru, city_en in zip(data["kz"][region_kk], data["ru"][region_ru], data["en"][region_en]):
                city, _ = City.objects.get_or_create(name_en=city_en, region=region)
                if city.name_kk != city_kz or city.name_ru != city_ru:  # type: ignore[attr-defined]
                    city.name_kk = city_kz  # type: ignore[attr-defined]
                    city.name_ru = city_ru  # type: ignore[attr-defined]
                    city.save()

        logger.info("All cities and regions for Kazakhstan have been created or already existed.")
