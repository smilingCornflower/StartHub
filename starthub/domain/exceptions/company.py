from domain.exceptions import CustomException
from domain.exceptions.repository import AlreadyExistsException, NotFoundException
from domain.exceptions.user import UserException
from domain.exceptions.validation import ValidationException


class CompanyException(CustomException):
    pass


class CompanyNotFoundException(NotFoundException, CompanyException):
    pass


class CompanyOwnershipRequiredException(CompanyException, UserException):
    pass


class CompanyNameIsTooLongException(ValidationException, CompanyException):
    pass


# ==== Business Number Exceptions ====
class BusinessNumberException(CustomException):
    pass


class BusinessNumberAlreadyExistsException(AlreadyExistsException, BusinessNumberException):
    pass


# ==== Company Founder Exceptions ====
class CompanyFounderException(CustomException):
    pass


class CompanyFounderNotFoundException(NotFoundException, CustomException):
    pass


class CompanyFounderAlreadyExistsException(AlreadyExistsException, CustomException):
    pass
