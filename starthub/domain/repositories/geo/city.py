from abc import ABC, abstractmethod

from domain.models.geo.city import City
from domain.ports.repository import AbstractReadRepository
from domain.value_objects.common import Id, Pagination
from domain.value_objects.filter import CityFilter


class CityReadRepository(AbstractReadRepository[City, CityFilter], ABC):
    @abstractmethod
    def get_by_id(self, id_: Id) -> City:
        pass

    @abstractmethod
    def get_all(self, filter_: CityFilter, pagination: Pagination | None = None) -> list[City]:
        pass
