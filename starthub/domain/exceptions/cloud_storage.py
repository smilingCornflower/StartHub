from domain.exceptions import DomainException


class CloudStorageException(DomainException):
    pass


class FileNotFoundCloudStorageException(CloudStorageException):
    pass
