from domain.exceptions import DomainException
from domain.exceptions.repository import AlreadyExistsException, NotFoundException
from domain.exceptions.validation import ValidationException


class ProjectException(DomainException):
    pass


class ProjectNameIsTooLongValidationException(ValidationException, ProjectException):
    pass


class NegativeProjectGoalSumValidationException(ValidationException, ProjectException):
    pass


class ProjectDeadlineInPastValidationException(ValidationException, ProjectException):
    pass


# Repository Exceptions
class ProjectNotFoundException(NotFoundException, ProjectException):
    pass


class ProjectNameAlreadyExistsException(AlreadyExistsException, ProjectException):
    pass
