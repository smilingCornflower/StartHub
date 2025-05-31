from domain.exceptions import DomainException
from domain.exceptions.repository import NotFoundException


class CountryException(DomainException):
    pass


class CountryNotFoundException(NotFoundException, CountryException):
    pass
