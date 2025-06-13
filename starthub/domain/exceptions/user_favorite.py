from domain.exceptions import DomainException
from domain.exceptions.repository import AlreadyExistsException, NotFoundException


class UserFavoriteException(DomainException):
    pass


class UserFavoriteNotFoundException(NotFoundException, UserFavoriteException):
    pass


class UserFavoriteAlreadyExistsException(AlreadyExistsException, UserFavoriteException):
    pass
