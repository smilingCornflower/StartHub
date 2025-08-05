from domain.exceptions import CustomException
from domain.exceptions.repository import NotFoundException


class RegionException(CustomException):
    pass


class RegionNotFoundException(NotFoundException, RegionException):
    pass
