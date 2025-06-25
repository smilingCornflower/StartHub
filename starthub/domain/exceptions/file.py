from domain.exceptions import DomainException


# ==== File Exceptions ====
class FileException(DomainException):
    pass


class NotPdfFileException(FileException):
    pass


class PdfFileTooLargeException(FileException):
    pass


# ==== Image Exception ====
class ImageException(FileException):
    pass


class NotSupportedImageFormatException(ImageException):
    pass


class ImageFileTooLargeException(ImageException):
    pass
