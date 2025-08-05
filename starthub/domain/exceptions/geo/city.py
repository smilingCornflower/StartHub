from domain.exceptions import CustomException
from domain.exceptions.repository import NotFoundException


class CityException(CustomException):
    pass


class CityNotFoundException(NotFoundException, CityException):
    pass
