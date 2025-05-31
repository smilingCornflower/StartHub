from domain.exceptions import DomainException
from domain.exceptions.repository import NotFoundException


class TeamMemberException(DomainException):
    pass


class TeamMemberNotFoundException(NotFoundException, TeamMemberException):
    pass
