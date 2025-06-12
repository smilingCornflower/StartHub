from domain.exceptions import DomainException
from domain.exceptions.repository import NotFoundException
from domain.exceptions.validation import ValidationException


class CountryException(DomainException):
    pass


class CountryNotFoundException(NotFoundException, CountryException):
    pass


class InvalidCountryCodeException(ValidationException, CountryException):
    pass
