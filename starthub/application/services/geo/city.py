from application.dto.geo import CityAllLangDto, CityDto
from application.ports.service import AbstractAppService
from domain.constants import DEFAULT_NOT_AVAILABLE
from domain.models.geo.city import City
from domain.repositories.geo.city import CityReadRepository
from domain.value_objects.common import Pagination
from domain.value_objects.filter import CityFilter
from domain.value_objects.geo import CityGetCommand


class CityAppService(AbstractAppService):
    def __init__(
        self,
        city_read_repository: CityReadRepository,
    ):
        self._city_read_repository = city_read_repository

    def get(self, command: CityGetCommand, pagination: Pagination | None = None) -> list[CityDto | CityAllLangDto]:
        city_filter: CityFilter = self._convert_command_to_filter(command=command)
        cities: list[City] = self._city_read_repository.get_all(filter_=city_filter, pagination=pagination)

        if command.all_languages is True:
            return [self._create_all_lang_dto(city=i) for i in cities]
        else:
            return [self._create_dto(city=i) for i in cities]

    def _convert_command_to_filter(self, command: CityGetCommand) -> CityFilter:
        return CityFilter(region_name=command.region_name)

    def _create_all_lang_dto(self, city: City) -> CityAllLangDto:
        return CityAllLangDto(
            id=city.id,
            name_kk=getattr(city, "name_kk", DEFAULT_NOT_AVAILABLE),
            name_ru=getattr(city, "name_ru", DEFAULT_NOT_AVAILABLE),
            name_en=getattr(city, "name_en", DEFAULT_NOT_AVAILABLE),
        )

    def _create_dto(self, city: City) -> CityDto:
        return CityDto(id=city.id, name=city.name)
