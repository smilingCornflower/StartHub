from application.dto.geo import RegionDto
from application.ports.service import AbstractAppService
from domain.repositories.geo.region import RegionReadRepository
from domain.value_objects.common import Pagination
from domain.value_objects.filter import RegionFilter


class RegionAppService(AbstractAppService):
    def __init__(
            self,
            region_read_repository: RegionReadRepository,
    ):
        self._region_read_repository = region_read_repository

    def get(self, filter_: RegionFilter, pagination: Pagination | None = None) -> list[RegionDto]:
        raise NotImplementedError("This method is not implemented yet.")