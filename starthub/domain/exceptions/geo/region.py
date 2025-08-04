from domain.exceptions import DomainException
from domain.exceptions.repository import NotFoundException


class RegionException(DomainException):
    pass


class RegionNotFoundException(NotFoundException, RegionException):
    pass
