from domain.exceptions import CustomException
from domain.exceptions.repository import NotFoundException


class NotificationException(CustomException):
    pass


class NotificationNotFounException(NotFoundException, NotificationException):
    pass
