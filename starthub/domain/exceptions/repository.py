from domain.exceptions import DomainException


class RepositoryException(DomainException):
    pass


class NotFoundException(RepositoryException):
    pass


class AlreadyExistsException(RepositoryException):
    pass
