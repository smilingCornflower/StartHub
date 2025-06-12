from datetime import date
from typing import Any

from domain.exceptions.validation import DateIsNotIsoFormatException, MissingRequiredFieldException
from loguru import logger


def get_required_field(data: dict[str, Any], field: str) -> Any:
    """:raises MissingRequiredFieldException:"""
    if field not in data:
        logger.exception(f"Missing required field: {field}.")
        raise MissingRequiredFieldException(f"Missing required field: {field}.")
    return data.get(field)


def parse_date(date_str: str) -> date:
    """:raises DateIsNotIsoFormatException:"""
    try:
        return date.fromisoformat(date_str)
    except ValueError as e:
        logger.exception(f"Exception during parsing established_date: {repr(e)}.")
        raise DateIsNotIsoFormatException("Date must be in iso format.") from e
