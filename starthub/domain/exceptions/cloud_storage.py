from domain.exceptions import CustomException


class CloudStorageException(CustomException):
    pass


class FileNotFoundCloudStorageException(CloudStorageException):
    pass
