from typing import cast

from django.http import QueryDict

from domain.value_objects.project.common import ProjectName
from domain.value_objects.search import ProjectSearchParams


def request_data_to_project_search_params(query: QueryDict) -> ProjectSearchParams:
    return ProjectSearchParams(name=ProjectName(value=cast(str, query["name"])) if "name" in query else None)
