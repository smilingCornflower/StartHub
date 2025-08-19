from django.http import QueryDict
from domain.value_objects.geo import RegionGetCommand
from rest_framework.request import Request


def request_to_region_get_command(request: Request) -> RegionGetCommand:
    params: QueryDict = request.query_params
    all_lang: bool = False
    if params.get("all_lang") == "true":
        all_lang = True
    return RegionGetCommand(all_languages=all_lang)
