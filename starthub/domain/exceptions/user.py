from domain.exceptions import DomainException
from domain.exceptions.repository import NotFoundException


class UserException(DomainException):
    pass


class UserNotFoundException(NotFoundException, UserException):
    pass


class EmailAlreadyExistsException(UserException):
    def __init__(self, email: str):
        super().__init__(f"Email {email} already exists.")


class PermissionException(UserException):
    pass


class ProfilePictureNotFoundException(NotFoundException, UserException):
    pass
