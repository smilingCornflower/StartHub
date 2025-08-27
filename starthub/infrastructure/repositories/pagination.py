from typing import TypeVar

from django.db.models.query import QuerySet
from domain.models.base import BaseModel
from domain.value_objects.common import CursorPagination, OffsetPagination

T = TypeVar("T", bound=BaseModel)


def _apply_cursor_pagination(queryset: QuerySet[T], pagination: CursorPagination) -> list[T]:
    if pagination.last_id is not None:
        queryset = queryset.filter(id__lt=pagination.last_id)

    return list(queryset.distinct()[: pagination.limit])


def _apply_offset_pagination(queryset: QuerySet[T], pagination: OffsetPagination) -> list[T]:
    limit = pagination.limit
    offset = pagination.offset

    return list(queryset[offset : offset + limit])


def apply_pagination(queryset: QuerySet[T], pagination: CursorPagination | OffsetPagination) -> list[T]:
    if isinstance(pagination, CursorPagination):
        return _apply_cursor_pagination(queryset=queryset, pagination=pagination)
    else:
        return _apply_offset_pagination(queryset=queryset, pagination=pagination)
