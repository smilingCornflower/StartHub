from domain.models.notification import Notification
from domain.ports.service import AbstractDomainService
from domain.repositories.notification import NotificationReadRepository, NotificationWriteRepository
from domain.value_objects.notification import NotificationCreatePayload


class NotificationService(AbstractDomainService):
    def __init__(self, read_repository: NotificationReadRepository, write_repository: NotificationWriteRepository):
        self._read_repository = read_repository
        self._write_repository = write_repository

    def create(self, payload: NotificationCreatePayload) -> Notification:
        return self._write_repository.create(data=payload)
