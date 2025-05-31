from domain.exceptions import DomainException
from domain.exceptions.repository import NotFoundException


class FundingModelException(DomainException):
    pass


class FundingModelNotFoundException(NotFoundException, FundingModelException):
    pass
