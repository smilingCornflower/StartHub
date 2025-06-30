from domain.exceptions.validation import MissingRequiredFieldException

APPLICATION_ERROR_CODES: dict[type, tuple[str, int]] = {
    MissingRequiredFieldException: ("MISSING_REQUIRED_FIELD", 400),
}
SUCCESS = "SUCCESS"
