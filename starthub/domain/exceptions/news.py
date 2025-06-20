from domain.exceptions import DomainException
from domain.exceptions.repository import NotFoundException
from domain.exceptions.validation import StringIsTooLongException, ValidationException


class NewsException(DomainException):
    pass


class NewsTitleIsTooLongException(ValidationException, NewsException):
    pass


class NewsContentIsTooLongException(StringIsTooLongException, NewsException):
    pass


class NewsNotFoundException(NotFoundException, NewsException):
    pass
