from typing import cast

from application.dto.geo import CityDto
from application.ports.service import AbstractAppService
from domain.constants import DEFAULT_NOT_AVAILABLE
from domain.enums.language import LangCodeEnum
from domain.models.geo.city import City
from domain.repositories.geo.city import CityReadRepository
from domain.value_objects.common import CursorPagination
from domain.value_objects.filter import CityFilter
from domain.value_objects.geo import CityGetCommand


class CityAppService(AbstractAppService):
    def __init__(
        self,
        city_read_repository: CityReadRepository,
    ):
        self._city_read_repository = city_read_repository

    def get(self, command: CityGetCommand, pagination: CursorPagination | None = None) -> list[CityDto]:
        city_filter: CityFilter = self._convert_command_to_filter(command=command)
        cities: list[City] = self._city_read_repository.get_all(filter_=city_filter, pagination=pagination)
        return [self._create_dto(languages=command.languages, city=c) for c in cities]

    @staticmethod
    def _create_dto(languages: list[LangCodeEnum], city: City) -> CityDto:
        names = {
            lang_code: cast(str, getattr(city, f"name_{lang_code}", DEFAULT_NOT_AVAILABLE)) for lang_code in languages
        }
        return CityDto(id=city.id, names=names)

    def _convert_command_to_filter(self, command: CityGetCommand) -> CityFilter:
        return CityFilter(region_name=command.region_name)
