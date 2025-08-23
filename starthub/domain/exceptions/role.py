from domain.exceptions import CustomException
from domain.exceptions.repository import NotFoundException


class RoleException(CustomException):
    pass


class RoleNotFoundException(NotFoundException, RoleException):
    pass
