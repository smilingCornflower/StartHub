from abc import ABC, abstractmethod

from domain.models.geo.address import Address
from domain.ports.repository import AbstractReadRepository, AbstractWriteRepository
from domain.value_objects.common import CursorPagination, Id, OffsetPagination
from domain.value_objects.filter import AddressFilter
from domain.value_objects.geo import AddressCreatePayload, AddressUpdatePayload


class AddressReadRepository(AbstractReadRepository[Address, AddressFilter, Id], ABC):
    @abstractmethod
    def get_by_id(self, id_: Id) -> Address:
        pass

    @abstractmethod
    def get_all(
        self, filter_: AddressFilter, pagination: CursorPagination | OffsetPagination | None = None
    ) -> list[Address]:
        pass


class AddressWriteRepository(AbstractWriteRepository[Address, AddressCreatePayload, AddressUpdatePayload, Id], ABC):
    @abstractmethod
    def create(self, data: AddressCreatePayload) -> Address:
        pass

    @abstractmethod
    def update(self, data: AddressUpdatePayload) -> Address:
        pass

    @abstractmethod
    def delete_by_id(self, id_: Id) -> None:
        pass
