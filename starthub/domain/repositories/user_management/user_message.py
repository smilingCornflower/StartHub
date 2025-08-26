from abc import ABC, abstractmethod

from domain.models.user_management.message import UserMessage
from domain.ports.repository import AbstractReadRepository, AbstractWriteRepository
from domain.value_objects.common import Pagination
from domain.value_objects.filter import UserMessageFilter
from domain.value_objects.user_management.user_message import (
    UserMessageCreatePayload,
    UserMessageId,
    UserMessageUpdatePayload,
)


class UserMessageReadRepository(AbstractReadRepository[UserMessage, UserMessageFilter, UserMessageId], ABC):
    @abstractmethod
    def get_by_id(self, id_: UserMessageId) -> UserMessage:
        pass

    @abstractmethod
    def get_all(self, filter_: UserMessageFilter, pagination: Pagination | None = None) -> list[UserMessage]:
        pass


class UserMessageWriteRepository(
    AbstractWriteRepository[UserMessage, UserMessageCreatePayload, UserMessageUpdatePayload, UserMessageId], ABC
):
    @abstractmethod
    def create(self, data: UserMessageCreatePayload) -> UserMessage:
        pass

    @abstractmethod
    def update(self, data: UserMessageUpdatePayload) -> UserMessage:
        pass

    @abstractmethod
    def delete_by_id(self, id_: UserMessageId) -> None:
        pass

    @abstractmethod
    def delete(self, message: UserMessage) -> None:
        pass
