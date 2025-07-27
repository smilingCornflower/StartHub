from typing import TypeVar

from django.db.models.query import QuerySet
from domain.models.base import BaseModel
from domain.value_objects.common import Pagination

T = TypeVar("T", bound=BaseModel)


def apply_pagination(queryset: QuerySet[T], pagination: Pagination) -> list[T]:
    if pagination and pagination.last_id is not None:
        queryset = queryset.filter(id__lt=pagination.last_id)

    if pagination and pagination.limit is not None:
        return list(queryset.distinct()[: pagination.limit])
    else:
        return list(queryset.distinct())
