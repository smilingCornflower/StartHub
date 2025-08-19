from application.ports.app_service_builder import AbstractAppServiceBuilder
from application.services.geo.city import CityAppService
from application.services.geo.region import RegionAppService
from infrastructure.repositories.geo.city import DjCityReadRepository
from infrastructure.repositories.geo.region import DjRegionReadRepository


class RegionAppServiceBuilder(AbstractAppServiceBuilder[RegionAppService]):
    @staticmethod
    def create_service() -> RegionAppService:
        return RegionAppService(region_read_repository=DjRegionReadRepository())


class CityAppServiceBuilder(AbstractAppServiceBuilder[CityAppService]):
    @staticmethod
    def create_service() -> CityAppService:
        return CityAppService(city_read_repository=DjCityReadRepository())
