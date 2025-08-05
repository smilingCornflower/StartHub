from domain.exceptions import CustomException


class ValidationException(CustomException):
    pass


class InvalidPhoneNumberException(ValidationException):
    pass


class InvalidSocialLinkException(ValidationException):
    pass


class DisallowedSocialLinkException(ValidationException):
    pass


class StringIsTooLongException(ValidationException):
    pass


class FirstNameIsTooLongException(StringIsTooLongException):
    pass


class LastNameIsTooLongException(StringIsTooLongException):
    pass


class EmptyStringException(ValidationException):
    pass


class DateIsNotIsoFormatException(ValidationException):
    pass


class DateInFutureException(ValidationException):
    pass


class InvalidEmailException(ValidationException):
    pass


class MissingRequiredFieldException(ValidationException):
    pass


class DeadlineInPastException(ValidationException):
    pass


class MissingFileExcpetion(ValidationException):
    pass
