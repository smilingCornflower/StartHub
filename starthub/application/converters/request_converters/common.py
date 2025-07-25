from datetime import date
from typing import cast

from django.http import QueryDict
from domain.exceptions.validation import DateIsNotIsoFormatException, MissingRequiredFieldException
from domain.value_objects.common import Pagination
from loguru import logger


def request_to_pagination(query_params: QueryDict) -> Pagination:
    logger.debug(f"request_data = {query_params}")
    return Pagination(
        last_id=int(cast(str, query_params.get("last_id"))) if "last_id" in query_params else None,
        limit=int(get_required_field(query_params, "limit")),
    )


def get_required_field[T](data: dict[str, T], field: str, field_name_in_exception: str | None = None) -> T:
    """:raises MissingRequiredFieldException:"""
    if field_name_in_exception is None:
        field_name_in_exception = field
    if field not in data:
        logger.exception(f"Missing required field: {field_name_in_exception}.")
        raise MissingRequiredFieldException(f"Missing required field: {field_name_in_exception}.")
    return data[field]


def parse_date(date_str: str) -> date:
    """:raises DateIsNotIsoFormatException:"""
    try:
        return date.fromisoformat(date_str)
    except ValueError as e:
        logger.exception(f"Exception during parsing established_date: {repr(e)}.")
        raise DateIsNotIsoFormatException("Date must be in iso format.") from e
