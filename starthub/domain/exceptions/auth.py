from domain.exceptions import DomainException
from domain.exceptions.validation import ValidationException


class AuthException(DomainException):
    pass


class InvalidCredentialsException(AuthException):
    pass


class InvalidTokenException(AuthException):
    pass


class TokenExpiredException(InvalidTokenException):
    pass


class WeakPasswordException(ValidationException, AuthException):
    pass
