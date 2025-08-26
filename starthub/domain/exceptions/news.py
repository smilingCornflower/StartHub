from domain.exceptions import CustomException
from domain.exceptions.repository import NotFoundException
from domain.exceptions.validation import StringIsTooLongException, ValidationException


class NewsException(CustomException):
    pass


class NewsTitleIsTooLongException(ValidationException, NewsException):
    pass


class NewsSubtitleIsTooLongException(ValidationException, NewsException):
    pass


class NewsContentIsTooLongException(StringIsTooLongException, NewsException):
    pass


class NewsNotFoundException(NotFoundException, NewsException):
    pass


class NewsImageMaxAmountException(ValidationException, NewsException):
    pass


class NewsImageContentAndFileMismatchException(ValidationException, NewsException):
    pass
