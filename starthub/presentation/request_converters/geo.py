from domain.value_objects.filter import RegionFilter
from rest_framework.request import Request


def request_to_region_filter(request: Request) -> RegionFilter:
    return RegionFilter()
