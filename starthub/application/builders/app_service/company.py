from application.builders.domain_service.address import AddressServiceBuilder
from application.builders.domain_service.company import CompanyServiceBuilder
from application.ports.app_service_builder import AbstractAppServiceBuilder
from application.services.company import CompanyAppService
from infrastructure.repositories.company import DjCompanyReadRepository
from infrastructure.repositories.geo.address import DjAddressWriteRepository
from infrastructure.repositories.user_management.user import DjUserReadRepository


class CompanyAppServiceBuilder(AbstractAppServiceBuilder[CompanyAppService]):
    @staticmethod
    def create_service() -> CompanyAppService:
        return CompanyAppService(
            company_service=CompanyServiceBuilder.create_service(),
            address_service=AddressServiceBuilder.create_service(),
            company_read_repository=DjCompanyReadRepository(),
            user_read_repository=DjUserReadRepository(),
            address_write_repository=DjAddressWriteRepository(),
        )
