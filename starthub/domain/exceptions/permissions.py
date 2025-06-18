from domain.exceptions import DomainException
from domain.exceptions.repository import NotFoundException


class PermissionException(DomainException):
    pass


class DeleteDeniedPermissionException(PermissionException):
    pass


class UpdateDeniedPermissionException(PermissionException):
    pass


class PermissionNotFoundException(NotFoundException, PermissionException):
    pass
