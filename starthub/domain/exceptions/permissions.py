from domain.exceptions import DomainException


class PermissionException(DomainException):
    pass


class DeleteDeniedPermissionException(PermissionException):
    pass


class UpdateDeniedPermissionException(PermissionException):
    pass
