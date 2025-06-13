from domain.exceptions.company import BusinessNumberAlreadyExistsException, CompanyFounderAlreadyExistsException
from domain.exceptions.country import CountryNotFoundException
from domain.models.company import Company, CompanyFounder
from domain.models.country import Country
from domain.repositories.company import (
    CompanyFounderReadRepository,
    CompanyFounderWriteRepository,
    CompanyReadRepository,
    CompanyWriteRepository,
)
from domain.repositories.country import CountryReadRepository
from domain.value_objects.common import Id
from domain.value_objects.company import CompanyCreateCommand, CompanyCreatePayload, CompanyFounderCreatePayload
from domain.value_objects.filter import CompanyFilter, CompanyFounderFilter, CountryFilter


class CompanyService:
    def __init__(
        self,
        company_write_repository: CompanyWriteRepository,
        country_read_repository: CountryReadRepository,
        company_read_repository: CompanyReadRepository,
    ):
        self._company_write_repository = company_write_repository
        self._country_read_repository = country_read_repository
        self._company_read_repository = company_read_repository

    def create(self, command: CompanyCreateCommand) -> Company:
        """
        :raises CountryNotFoundException:
        :raises UserNotFoundException:
        :raises BusinessNumberAlreadyExistsException:
        """
        search_result: list[Company] = self._company_read_repository.get_all(
            CompanyFilter(business_id=command.business_id)
        )
        if search_result:
            raise BusinessNumberAlreadyExistsException("This business number already exists.")

        countries: list[Country] = self._country_read_repository.get_all(CountryFilter(code=command.country_code))
        if not countries:
            raise CountryNotFoundException(f"A country with code = {command.country_code.value} not found.")
        country: Country = countries[0]

        return self._company_write_repository.create(
            CompanyCreatePayload(
                name=command.name,
                project_id=command.project_id,
                country_id=Id(value=country.id),
                business_id=command.business_id,
                established_date=command.established_date,
                description=command.description,
            )
        )


class CompanyFounderService:
    def __init__(
        self,
        company_founder_write_repository: CompanyFounderWriteRepository,
        company_founder_read_repository: CompanyFounderReadRepository,
    ):
        self._company_founder_write_repository = company_founder_write_repository
        self._company_founder_read_repository = company_founder_read_repository

    def create(self, payload: CompanyFounderCreatePayload) -> CompanyFounder:
        search_result: list[CompanyFounder] = self._company_founder_read_repository.get_all(
            filter_=CompanyFounderFilter(company_id=payload.company_id)
        )
        if search_result:
            raise CompanyFounderAlreadyExistsException(
                f"Company founder for the company with id = {payload.company_id.value} already exists."
            )

        return self._company_founder_write_repository.create(payload)
