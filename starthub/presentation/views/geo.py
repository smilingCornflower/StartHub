from dataclasses import asdict

from application.dto.geo import RegionDto
from application.services.gateway import gateway
from config.settings import BASE_DIR
from django.utils.translation import get_language
from loguru import logger
from presentation.request_converters.geo import request_to_city_get_command, request_to_region_get_command
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

cities_and_regions_json_path = BASE_DIR / "../fixtures/kazakhstan_cities_by_region.json"


class CityView(APIView):
    @staticmethod
    def get(request: Request) -> Response:
        print()
        logger.info("GET /cities/")
        logger.debug(f"Current language = {get_language()}")

        command = request_to_city_get_command(request=request)
        cities = gateway.city_app_service.get(command=command)
        return Response(map(asdict, cities))


class RegionView(APIView):
    @staticmethod
    def get(request: Request) -> Response:
        print()
        logger.info("GET /regions/")
        logger.debug(f"Current language = {get_language()}")

        command = request_to_region_get_command(request=request)
        regions: list[RegionDto] = gateway.region_app_service.get(command=command)
        return Response(map(asdict, regions))
