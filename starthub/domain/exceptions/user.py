from domain.exceptions import DomainException
from domain.exceptions.repository import NotFoundException


class UserException(DomainException):
    pass


class UserNotFoundException(NotFoundException, UserException):
    pass


class UsernameAlreadyExistsException(UserException):
    def __init__(self, username: str):
        super().__init__(f"Username {username} already exists.")


class EmailAlreadyExistsException(UserException):
    def __init__(self, email: str):
        super().__init__(f"Email {email} already exists.")


class PermissionException(UserException):
    pass
