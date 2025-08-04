from application.ports.domain_service_builder import AbstractDomainServiceBuilder
from domain.services.address import AddressService
from infrastructure.repositories.geo.address import DjAddressWriteRepository
from infrastructure.repositories.geo.country import DjCountryReadRepository


class AddressServiceBuilder(AbstractDomainServiceBuilder[AddressService]):
    @staticmethod
    def create_service() -> AddressService:
        return AddressService(
            write_repository=DjAddressWriteRepository(),
            country_read_repositroy=DjCountryReadRepository(),
        )
