from domain.exceptions import CustomException


# ==== File Exceptions ====
class FileException(CustomException):
    pass


class UnsupportedFileExtensionException(CustomException):
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


# ==== Video Exception ====
class VideoException(FileException):
    pass


class NotSupportedVideoFormatException(VideoException):
    pass


class VideoFileTooLargeException(VideoException):
    pass
