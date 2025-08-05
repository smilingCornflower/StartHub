from domain.exceptions import CustomException


# ==== File Exceptions ====
class FileException(CustomException):
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
