from domain.exceptions import CustomException
from domain.exceptions.repository import NotFoundException


class PermissionException(CustomException):
    pass


class ViewDeniedPermissionException(PermissionException):
    pass


class AddDeniedPermissionException(PermissionException):
    pass


class DeleteDeniedPermissionException(PermissionException):
    pass


class UpdateDeniedPermissionException(PermissionException):
    pass


class PermissionNotFoundException(NotFoundException, PermissionException):
    pass
