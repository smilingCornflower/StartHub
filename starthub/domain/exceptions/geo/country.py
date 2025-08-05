from domain.exceptions import CustomException
from domain.exceptions.repository import NotFoundException
from domain.exceptions.validation import ValidationException


class CountryException(CustomException):
    pass


class CountryNotFoundException(NotFoundException, CountryException):
    pass


class InvalidCountryCodeException(ValidationException, CountryException):
    pass
