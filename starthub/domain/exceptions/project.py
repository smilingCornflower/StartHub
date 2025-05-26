from domain.exceptions import DomainException


class ProjectException(DomainException):
    pass


class ProjectNotFoundException(ProjectException):
    pass


class ProjectDeletionForbiddenException(ProjectException):
    pass
