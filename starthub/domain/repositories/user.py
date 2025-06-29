from abc import ABC, abstractmethod

from domain.models.user import User, UserPhone
from domain.ports.repository import AbstractReadRepository, AbstractWriteRepository
from domain.value_objects.common import Id, Pagination, PhoneNumber
from domain.value_objects.filter import UserFilter, UserPhoneFilter
from domain.value_objects.user import (
    Email,
    UserCreatePayload,
    UserPhoneCreatePayload,
    UserPhoneUpdatePayload,
    UserUpdatePayload,
)


class UserReadRepository(AbstractReadRepository[User, UserFilter]):
    @abstractmethod
    def get_by_id(self, id_: Id) -> User:
        """:raises UserNotFoundException:"""
        pass

    @abstractmethod
    def get_all(self, filter_: UserFilter, pagination: Pagination | None = None) -> list[User]:
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


class UserPhoneReadRepository(AbstractReadRepository[UserPhone, UserPhoneFilter], ABC):
    @abstractmethod
    def get_by_id(self, id_: Id) -> UserPhone:
        pass

    @abstractmethod
    def get_all(self, filter_: UserPhoneFilter, pagination: Pagination | None = None) -> list[UserPhone]:
        pass


class UserPhoneWriteRepository(AbstractWriteRepository[UserPhone, UserPhoneCreatePayload, UserPhoneUpdatePayload], ABC):
    @abstractmethod
    def create(self, data: UserPhoneCreatePayload) -> UserPhone:
        pass

    @abstractmethod
    def update(self, data: UserPhoneUpdatePayload) -> UserPhone:
        pass

    @abstractmethod
    def delete_by_id(self, id_: Id) -> None:
        pass

    @abstractmethod
    def delete_by_phone(self, phone: PhoneNumber) -> None:
        pass
