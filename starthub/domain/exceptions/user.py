from domain.exceptions import CustomException
from domain.exceptions.repository import AlreadyExistsException, NotFoundException


class UserException(CustomException):
    pass


class UserNotFoundException(NotFoundException, UserException):
    pass


class UserDeactivedException(UserException):
    pass


class EmailAlreadyExistsException(AlreadyExistsException, UserException):
    def __init__(self, email: str):
        super().__init__(f"Email {email} already exists.")


class PermissionException(UserException):
    pass


class ProfilePictureNotFoundException(NotFoundException, UserException):
    pass


# ==== UserPhoneExceptions ====
class UserPhoneException(UserException):
    pass


class UserPhoneAlreadyExistException(AlreadyExistsException, UserPhoneException):
    def __init__(self, phone: str):
        super().__init__(f"UserPhone {phone} already exists.")


class UserPhoneNotFoundException(NotFoundException, UserPhoneException):
    pass
