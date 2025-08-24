from domain.exceptions import CustomException
from domain.exceptions.repository import NotFoundException
from domain.exceptions.validation import StringIsTooLongException, ValidationException


class UserMessageException(CustomException):
    pass


class UserMessageNotFoundException(NotFoundException, UserMessageException):
    pass


class UserUnreadMessageMaxAmountException(ValidationException, UserMessageException):
    pass


class UserMessageTopicIsTooLongException(StringIsTooLongException, UserMessageException):
    pass


class UserMessageContentIsTooLongException(StringIsTooLongException, UserMessageException):
    pass
