from typing import cast

from django.http import QueryDict
from domain.value_objects.geo import CityGetCommand, RegionGetCommand, RegionName
from loguru import logger
from rest_framework.request import Request


def request_to_region_get_command(request: Request) -> RegionGetCommand:
    params: QueryDict = request.query_params
    all_lang: bool = False
    if params.get("all_lang") == "true":
        all_lang = True
    return RegionGetCommand(all_languages=all_lang)


def request_to_city_get_command(request: Request) -> CityGetCommand:
    params: QueryDict = request.query_params

    all_lang: bool = False
    if params.get("all_lang") == "true":
        all_lang = True

    region: RegionName | None = RegionName(value=cast(str, params["region"])) if "region" in params else None

    command = CityGetCommand(all_languages=all_lang, region_name=region)
    logger.debug(f"command = {command}")
    return command
