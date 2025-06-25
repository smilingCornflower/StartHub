from abc import ABC, abstractmethod

from domain.models.user import User
from domain.ports.repository import AbstractReadRepository, AbstractWriteRepository
from domain.value_objects.common import Id
from domain.value_objects.filter import UserFilter
from domain.value_objects.user import Email, UserCreatePayload, UserUpdatePayload


class UserReadRepository(AbstractReadRepository[User, UserFilter]):
    @abstractmethod
    def get_by_id(self, id_: Id) -> User:
        """:raises UserNotFoundException:"""
        pass

    @abstractmethod
    def get_all(self, filter_: UserFilter) -> list[User]:
        pass

    @abstractmethod
    def get_by_email(self, email: Email) -> User:
        """:raises UserNotFoundException:"""
        pass


class UserWriteRepository(AbstractWriteRepository[User, UserCreatePayload, UserUpdatePayload], ABC):
    @abstractmethod
    def create(self, data: UserCreatePayload) -> User:
        pass

    @abstractmethod
    def update(self, data: UserUpdatePayload) -> User:
        """:raises UserNotFoundException:"""
        pass

    @abstractmethod
    def delete_by_id(self, id_: Id) -> None:
        """:raises UserNotFoundException:"""
        pass

    @abstractmethod
    def update_last_login(self, user: User) -> None:
        pass
