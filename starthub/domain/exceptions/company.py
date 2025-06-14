from domain.exceptions import DomainException
from domain.exceptions.repository import AlreadyExistsException, NotFoundException
from domain.exceptions.user import UserException
from domain.exceptions.validation import ValidationException


class CompanyException(DomainException):
    pass


class CompanyNotFoundException(NotFoundException, CompanyException):
    pass


class CompanyOwnershipRequiredException(CompanyException, UserException):
    pass


class CompanyNameIsTooLongException(ValidationException, CompanyException):
    pass


# ==== Business Number Exceptions ====
class BusinessNumberException(DomainException):
    pass


class BusinessNumberAlreadyExistsException(AlreadyExistsException, BusinessNumberException):
    pass


# ==== Company Founder Exceptions ====
class CompanyFounderException(DomainException):
    pass


class CompanyFounderNotFoundException(NotFoundException, DomainException):
    pass


class CompanyFounderAlreadyExistsException(AlreadyExistsException, DomainException):
    pass
