from domain.exceptions import DomainException


class ImageException(DomainException):
    pass


class InvalidImageException(ImageException):
    pass


class NotSupportedImageFormatException(InvalidImageException):
    pass
