from domain.exceptions import DomainException
from domain.exceptions.repository import NotFoundException


class ProjectCategoryException(DomainException):
    pass


class ProjectCategoryNotFoundException(NotFoundException, ProjectCategoryException):
    pass
