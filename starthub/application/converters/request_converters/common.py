from datetime import date
from typing import Any

from domain.exceptions.validation import DateIsNotIsoFormatException, MissingRequiredFieldException
from domain.value_objects.common import Pagination
from loguru import logger


def request_to_pagination(request_data: dict[str, Any]) -> Pagination:
    return Pagination(
        last_id=request_data["last_id"] if "last_id" in request_data else None,
        limit=get_required_field(request_data, "limit"),
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
