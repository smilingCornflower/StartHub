from application.ports.service_factory import AbstractServiceFactory
from application.services.company import CompanyAppService
from domain.services.company import CompanyService
from domain.services.country import CountryService
from infrastructure.repositories.company import DjCompanyWriteRepository
from infrastructure.repositories.country import DjCountryReadRepository
from infrastructure.repositories.user import DjUserReadRepository


class CompanyServiceFactory(AbstractServiceFactory[CompanyAppService]):
    @staticmethod
    def create_service() -> CompanyAppService:
        return CompanyAppService(
            company_service=CompanyService(
                company_write_repository=DjCompanyWriteRepository(),
                user_read_repository=DjUserReadRepository(),
            ),
            country_service=CountryService(
                country_read_repository=DjCountryReadRepository(),
            ),
        )
