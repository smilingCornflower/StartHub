from domain.exceptions import DomainException
from domain.exceptions.repository import AlreadyExistsException, NotFoundException


class ProjectSocialLinkException(DomainException):
    pass


class ProjectSocialLinkNotFoundException(NotFoundException, ProjectSocialLinkException):
    pass


class ProjectSocialLinkAlreadyExistsException(AlreadyExistsException, ProjectSocialLinkException):
    pass
