from domain.exceptions import DomainException
from domain.exceptions.repository import NotFoundException
from domain.exceptions.user import UserException


class CompanyException(DomainException):
    pass


class CompanyNotFoundException(NotFoundException, CompanyException):
    pass


class CompanyOwnershipRequiredException(CompanyException, UserException):
    pass
