from typing import cast

from django.http import QueryDict
from loguru import logger
from rest_framework.request import Request

from domain.value_objects.geo import CityGetCommand, RegionGetCommand, RegionName
from presentation.request_converters.common import parse_languages


def request_to_region_get_command(request: Request) -> RegionGetCommand:
    languages = parse_languages(request=request)
    return RegionGetCommand(languages=languages)


def request_to_city_get_command(request: Request) -> CityGetCommand:
    params: QueryDict = request.query_params

    languages = parse_languages(request=request)
    logger.debug(f"{languages=}")

    region: RegionName | None = RegionName(value=cast(str, params["region"])) if "region" in params else None

    command = CityGetCommand(languages=languages, region_name=region)

    logger.debug(f"command = {command}")
    return command
