from application.builders.domain_service.permission import PermissionServiceBuilder
from application.ports.domain_service_builder import AbstractDomainServiceBuilder
from domain.services.company import CompanyService
from infrastructure.repositories.company import DjCompanyReadRepository, DjCompanyWriteRepository
from infrastructure.repositories.geo.address import DjAddressWriteRepository
from infrastructure.repositories.geo.country import DjCountryReadRepository


class CompanyServiceBuilder(AbstractDomainServiceBuilder[CompanyService]):
    @staticmethod
    def create_service() -> CompanyService:
        return CompanyService(
            company_read_repository=DjCompanyReadRepository(),
            country_read_repository=DjCountryReadRepository(),
            company_write_repository=DjCompanyWriteRepository(),
            address_write_repository=DjAddressWriteRepository(),
            permission_service=PermissionServiceBuilder.create_service(),
        )
