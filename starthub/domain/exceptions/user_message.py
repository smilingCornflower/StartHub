from domain.exceptions import CustomException
from domain.exceptions.repository import NotFoundException


class UserMessageException(CustomException):
    pass


class UserMessageNotFoundException(NotFoundException, UserMessageException):
    pass
