from abc import ABC, abstractmethod

from domain.models.geo.country import Country
from domain.ports.repository import AbstractReadRepository
from domain.value_objects.common import CursorPagination, Id, OffsetPagination
from domain.value_objects.country import CountryCode
from domain.value_objects.filter import CountryFilter


class CountryReadRepository(AbstractReadRepository[Country, CountryFilter, Id], ABC):
    @abstractmethod
    def get_by_id(self, id_: Id) -> Country:
        """:raises CountryNotFoundException:"""
        pass

    @abstractmethod
    def get_all(
        self, filter_: CountryFilter, pagination: CursorPagination | OffsetPagination | None = None
    ) -> list[Country]:
        pass

    @abstractmethod
    def get_by_code(self, code: CountryCode) -> Country:
        """:raises CountryNotFoundException:"""
        pass
