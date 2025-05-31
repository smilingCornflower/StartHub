from domain.exceptions import DomainException


class PermissionException(DomainException):
    pass


class DeletePermissionDenied(PermissionException):
    pass
