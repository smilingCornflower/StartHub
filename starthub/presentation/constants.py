import pydantic

from domain.exceptions.auth import InvalidTokenException, TokenExpiredException
from domain.exceptions.validation import (
    DateIsNotIsoFormatException,
    EmptyStringException,
    MissingRequiredFieldException,
)

APPLICATION_ERROR_CODES: dict[type, tuple[str, int]] = {
    MissingRequiredFieldException: ("MISSING_REQUIRED_FIELD", 400),
    pydantic.ValidationError: ("INVALID_DATA_TYPE", 400),
    EmptyStringException: ("EMPTY_VALUE_NOT_ALLOWED", 422),
    TokenExpiredException: ("TOKEN_EXPIRED", 401),
    InvalidTokenException: ("INVALID_TOKEN", 401),
    DateIsNotIsoFormatException: ("DATE_IS_NOT_ISO_FORMAT", 422),
}
SUCCESS = "SUCCESS"
