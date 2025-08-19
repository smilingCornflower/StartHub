from application.dto.geo import RegionDto
from application.ports.service import AbstractAppService
from domain.models.geo.region import Region
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
        regions = self._region_read_repository.get_all(filter_=filter_, pagination=pagination)
        return [self._create_dto(region=i) for i in regions]

    def _create_dto(self, region: Region) -> RegionDto:
        return RegionDto(id=region.id, name=region.name)
