from domain.exceptions import DomainException
from domain.exceptions.repository import AlreadyExistsException, NotFoundException


class ProjectPhoneException(DomainException):
    pass


class ProjectPhoneAlreadyExistsException(AlreadyExistsException, ProjectPhoneException):
    pass


class ProjectPhoneNotFoundException(NotFoundException, ProjectPhoneException):
    pass
