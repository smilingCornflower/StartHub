from application.ports.app_service_builder import AbstractAppServiceBuilder
from application.services.geo.region import RegionAppService
from infrastructure.repositories.geo.region import DjRegionReadRepository


class RegionAppServiceBuilder(AbstractAppServiceBuilder[RegionAppService]):
    @staticmethod
    def create_service() -> RegionAppService:
        return RegionAppService(region_read_repository=DjRegionReadRepository())
