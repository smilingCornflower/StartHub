from domain.exceptions import CustomException


class RepositoryException(CustomException):
    pass


class NotFoundException(RepositoryException):
    pass


class AlreadyExistsException(RepositoryException):
    pass
