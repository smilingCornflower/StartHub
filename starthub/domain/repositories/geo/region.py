from abc import ABC, abstractmethod

from domain.models.geo.region import Region
from domain.ports.repository import AbstractReadRepository
from domain.value_objects.common import Pagination
from domain.value_objects.filter import RegionFilter
from domain.value_objects.geo import RegionId


class RegionReadRepository(AbstractReadRepository[Region, RegionFilter, RegionId], ABC):
    @abstractmethod
    def get_by_id(self, id_: RegionId) -> Region:
        pass

    @abstractmethod
    def get_all(self, filter_: RegionFilter, pagination: Pagination | None = None) -> list[Region]:
        pass
