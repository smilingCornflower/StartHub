from abc import ABC, abstractmethod

from domain.models.geo.city import City
from domain.ports.repository import AbstractReadRepository
from domain.value_objects.common import CursorPagination, OffsetPagination
from domain.value_objects.filter import CityFilter
from domain.value_objects.geo import CityId


class CityReadRepository(AbstractReadRepository[City, CityFilter, CityId], ABC):
    @abstractmethod
    def get_by_id(self, id_: CityId) -> City:
        pass

    @abstractmethod
    def get_all(self, filter_: CityFilter, pagination: CursorPagination | OffsetPagination | None = None) -> list[City]:
        pass
