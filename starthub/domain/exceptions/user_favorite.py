from domain.exceptions import CustomException
from domain.exceptions.repository import AlreadyExistsException, NotFoundException


class UserFavoriteException(CustomException):
    pass


class UserFavoriteNotFoundException(NotFoundException, UserFavoriteException):
    pass


class UserFavoriteAlreadyExistsException(AlreadyExistsException, UserFavoriteException):
    pass
