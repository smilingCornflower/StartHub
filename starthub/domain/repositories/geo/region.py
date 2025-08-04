from abc import ABC, abstractmethod

from domain.models.geo.region import Region
from domain.ports.repository import AbstractReadRepository
from domain.value_objects.common import Id, Pagination
from domain.value_objects.filter import RegionFilter


class RegionReadRepository(AbstractReadRepository[Region, RegionFilter], ABC):
    @abstractmethod
    def get_by_id(self, id_: Id) -> Region:
        pass

    @abstractmethod
    def get_all(self, filter_: RegionFilter, pagination: Pagination | None = None) -> list[Region]:
        pass
