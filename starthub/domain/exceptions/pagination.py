from domain.exceptions import DomainException


class PaginationException(DomainException):
    pass


class PaginationMaxLimitException(PaginationException):
    pass
