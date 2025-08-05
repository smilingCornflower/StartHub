from domain.exceptions import CustomException
from domain.exceptions.validation import MissingRequiredFieldException, ValidationException


class AuthException(CustomException):
    pass


class InvalidCredentialsException(AuthException):
    pass


class InvalidTokenException(AuthException):
    pass


class TokenExpiredException(InvalidTokenException):
    pass


class PasswordValidationException(ValidationException, AuthException):
    pass


class MissingAccessTokenException(MissingRequiredFieldException, AuthException):
    pass
