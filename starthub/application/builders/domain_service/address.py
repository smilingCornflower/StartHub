from application.builders.domain_service.permission import PermissionServiceBuilder
from application.ports.domain_service_builder import AbstractDomainServiceBuilder
from domain.services.address import AddressService
from infrastructure.repositories.geo.address import DjAddressReadRepository, DjAddressWriteRepository
from infrastructure.repositories.geo.city import DjCityReadRepository
from infrastructure.repositories.geo.country import DjCountryReadRepository


class AddressServiceBuilder(AbstractDomainServiceBuilder[AddressService]):
    @staticmethod
    def create_service() -> AddressService:
        return AddressService(
            read_repository=DjAddressReadRepository(),
            write_repository=DjAddressWriteRepository(),
            country_read_repositroy=DjCountryReadRepository(),
            city_read_repository=DjCityReadRepository(),
            permission_service=PermissionServiceBuilder.create_service(),
        )
