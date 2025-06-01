from domain.exceptions import DomainException
from domain.exceptions.repository import AlreadyExistsException, NotFoundException
from domain.exceptions.validation import ValidationException


class ProjectCategoryException(DomainException):
    pass


class ProjectCategoryNotFoundException(NotFoundException, ProjectCategoryException):
    pass


class ProjectPhoneException(DomainException):
    pass


class ProjectPhoneAlreadyExistsException(AlreadyExistsException, ProjectPhoneException):
    pass


class ProjectPhoneNotFoundException(NotFoundException, ProjectPhoneException):
    pass


class ProjectSocialLinkException(DomainException):
    pass


class ProjectSocialLinkNotFoundException(NotFoundException, ProjectSocialLinkException):
    pass


class ProjectSocialLinkAlreadyExistsException(AlreadyExistsException, ProjectSocialLinkException):
    pass


class TeamMemberException(DomainException):
    pass


class TeamMemberNotFoundException(NotFoundException, TeamMemberException):
    pass


class ProjectException(DomainException):
    pass


class ProjectNameIsTooLongValidationException(ValidationException, ProjectException):
    pass


class NegativeProjectGoalSumValidationException(ValidationException, ProjectException):
    pass


class ProjectDeadlineInPastValidationException(ValidationException, ProjectException):
    pass


class ProjectNotFoundException(NotFoundException, ProjectException):
    pass


class ProjectNameAlreadyExistsException(AlreadyExistsException, ProjectException):
    pass


class FundingModelException(DomainException):
    pass


class FundingModelNotFoundException(NotFoundException, FundingModelException):
    pass
