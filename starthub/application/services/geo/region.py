from application.dto.geo import RegionAllLangDto, RegionDto
from application.ports.service import AbstractAppService
from domain.constants import DEFAULT_NOT_AVAILABLE
from domain.models.geo.region import Region
from domain.repositories.geo.region import RegionReadRepository
from domain.value_objects.common import Pagination
from domain.value_objects.filter import RegionFilter
from domain.value_objects.geo import RegionGetCommand


class RegionAppService(AbstractAppService):
    def __init__(
        self,
        region_read_repository: RegionReadRepository,
    ):
        self._region_read_repository = region_read_repository

    def get(
        self, command: RegionGetCommand, pagination: Pagination | None = None
    ) -> list[RegionDto | RegionAllLangDto]:
        region_filter = self.convert_command_to_filter(command=command)
        regions = self._region_read_repository.get_all(filter_=region_filter, pagination=pagination)

        if command.all_languages is True:
            return [self._create_all_lang_dto(region=i) for i in regions]
        else:
            return [self._create_dto(region=i) for i in regions]

    def _create_all_lang_dto(self, region: Region) -> RegionAllLangDto:
        return RegionAllLangDto(
            id=region.id,
            name_kk=getattr(region, "name_kk", DEFAULT_NOT_AVAILABLE),
            name_ru=getattr(region, "name_ru", DEFAULT_NOT_AVAILABLE),
            name_en=getattr(region, "name_en", DEFAULT_NOT_AVAILABLE),
        )

    def _create_dto(self, region: Region) -> RegionDto:
        return RegionDto(id=region.id, name=region.name)

    def convert_command_to_filter(self, command: RegionGetCommand) -> RegionFilter:
        return RegionFilter()
