from domain.exceptions import CustomException


class PaginationException(CustomException):
    pass


class PaginationMaxLimitException(PaginationException):
    pass
