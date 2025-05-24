from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from domain.ports.filter import AbstractFilter
from domain.ports.model import AbstractModel
from domain.ports.payload import AbstractCreatePayload, AbstractUpdatePayload
from domain.value_objects.common import Id

T = TypeVar("T", bound=AbstractModel)
F = TypeVar("F", bound=AbstractFilter)
C = TypeVar("C", bound=AbstractCreatePayload)
U = TypeVar("U", bound=AbstractUpdatePayload)


class AbstractReadRepository(ABC, Generic[T, F]):
    @abstractmethod
    def get_by_id(self, id_: Id) -> T:
        pass

    @abstractmethod
    def get_all(self, filter_: F) -> list[T]:
        pass


class AbstractWriteRepository(ABC, Generic[T, C, U]):
    @abstractmethod
    def create(self, data: C) -> T:
        pass

    @abstractmethod
    def update(self, data: U) -> T:
        pass

    @abstractmethod
    def delete(self, id_: Id) -> None:
        pass
