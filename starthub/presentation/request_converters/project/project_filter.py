from pprint import pformat
from typing import cast

from django.http import QueryDict
from domain.value_objects.common import Id, Slug
from domain.value_objects.filter import ProjectFilter
from domain.value_objects.project.common import ProjectStageVo, ProjectStatus
from loguru import logger
from rest_framework.request import Request


def request_to_project_filter(request: Request) -> ProjectFilter:
    params: QueryDict = request.query_params
    logger.debug(f"params = {pformat(params)}")

    filter_ = ProjectFilter()
    if params.get("category_slug"):
        filter_.category_slug = Slug(value=cast(str, params.get("category_slug")))
    if params.get("funding_model_slug"):
        filter_.funding_model_slug = Slug(value=cast(str, params.get("funding_model_slug")))
    if params.get("status"):
        filter_.statuses = [ProjectStatus(value=status) for status in params.getlist("status")]
    if params.get("stage"):
        filter_.stage = ProjectStageVo(value=cast(str, params.get("stage")))
    if params.get("user_id"):
        filter_.user_id = Id(value=int(cast(str, params["user_id"])))

    return filter_
