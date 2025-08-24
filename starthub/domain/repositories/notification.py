from abc import ABC, abstractmethod

from domain.models.notification import Notification
from domain.ports.repository import AbstractReadRepository, AbstractWriteRepository
from domain.value_objects.common import Pagination
from domain.value_objects.filter import NotificationFilter
from domain.value_objects.notification import NotificationCreatePayload, NotificationId, NotificationUpdatePayload


class NotificationReadRepository(AbstractReadRepository[Notification, NotificationFilter, NotificationId], ABC):
    @abstractmethod
    def get_by_id(self, id_: NotificationId) -> Notification:
        pass

    @abstractmethod
    def get_all(self, filter_: NotificationFilter, pagination: Pagination | None = None) -> list[Notification]:
        pass


class NotificationWriteRepository(
    AbstractWriteRepository[Notification, NotificationCreatePayload, NotificationUpdatePayload, NotificationId], ABC
):
    @abstractmethod
    def create(self, data: NotificationCreatePayload) -> Notification:
        pass

    @abstractmethod
    def update(self, data: NotificationUpdatePayload) -> Notification:
        pass

    @abstractmethod
    def delete_by_id(self, id_: NotificationId) -> None:
        pass
