from domain.exceptions import DomainException


class ValidationException(DomainException):
    pass


class InvalidPhoneNumberException(ValidationException):
    pass


class InvalidSocialLinkException(ValidationException):
    pass


class DisallowedSocialLinkException(ValidationException):
    pass


class FirstNameIsTooLongException(ValidationException):
    pass


class LastNameIsTooLongException(ValidationException):
    pass


class EmptyStringException(ValidationException):
    pass


class DateIsNotIsoFormatException(ValidationException):
    pass


class InvalidEmailException(ValidationException):
    pass


class MissingRequiredFieldException(ValidationException):
    pass
