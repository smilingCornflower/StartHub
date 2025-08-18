import json

from config.settings import BASE_DIR
from loguru import logger
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

cities_and_regions_json_path = BASE_DIR / "../fixtures/kazakhstan_cities_by_region.json"


class CityView(APIView):
    @staticmethod
    def get(request: Request) -> Response:
        print()
        logger.info("GET /cities/")

        with open(cities_and_regions_json_path) as f:
            data: dict[str, list[str]] = json.load(f)

        region: str | None = request.query_params.get("region")
        logger.debug(f"region = {region}")

        if region is None:
            logger.debug("Returning all cities without region filter")
            all_cities = sum(data.values(), [])
            return Response(all_cities)
        else:
            logger.debug(f"Returning cities for region: {region}")
            return Response(data[region])


class RegionView(APIView):
    @staticmethod
    def get(request: Request) -> Response:
        print()
        logger.info("GET /regions/")

        with open(cities_and_regions_json_path) as f:
            data = json.load(f)
            return Response(list(data))
