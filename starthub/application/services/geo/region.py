from typing import cast

from application.dto.geo import RegionDto
from application.ports.service import AbstractAppService
from domain.constants import DEFAULT_NOT_AVAILABLE
from domain.enums.language import LangCodeEnum
from domain.models.geo.region import Region
from domain.repositories.geo.region import RegionReadRepository
from domain.value_objects.common import CursorPagination
from domain.value_objects.filter import RegionFilter
from domain.value_objects.geo import RegionGetCommand


class RegionAppService(AbstractAppService):
    def __init__(
        self,
        region_read_repository: RegionReadRepository,
    ):
        self._region_read_repository = region_read_repository

    def get(self, command: RegionGetCommand, pagination: CursorPagination | None = None) -> list[RegionDto]:
        region_filter = self._convert_command_to_filter(command=command)
        regions = self._region_read_repository.get_all(filter_=region_filter, pagination=pagination)
        return [self._create_dto(region=region, languages=command.languages) for region in regions]

    def _create_dto(self, region: Region, languages: list[LangCodeEnum]) -> RegionDto:
        names = {
            lang_code: cast(str, getattr(region, f"name_{lang_code}", DEFAULT_NOT_AVAILABLE)) for lang_code in languages
        }
        return RegionDto(id=region.id, names=names)

    def _convert_command_to_filter(self, command: RegionGetCommand) -> RegionFilter:
        return RegionFilter()
