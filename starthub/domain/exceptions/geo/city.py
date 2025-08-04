from domain.exceptions import DomainException
from domain.exceptions.repository import NotFoundException


class CityException(DomainException):
    pass


class CityNotFoundException(NotFoundException, CityException):
    pass
