from domain.exceptions.company import BusinessNumberAlreadyExistsException
from domain.exceptions.country import CountryNotFoundException
from domain.models.company import Company, CompanyFounder
from domain.models.country import Country
from domain.repositories.company import CompanyFounderWriteRepository, CompanyReadRepository, CompanyWriteRepository
from domain.repositories.country import CountryReadRepository
from domain.repositories.user import UserReadRepository
from domain.value_objects.common import Id
from domain.value_objects.company import CompanyCreateCommand, CompanyCreatePayload
from domain.value_objects.filter import CompanyFilter, CountryFilter
from loguru import logger


class CompanyService:
    def __init__(
        self,
        company_write_repository: CompanyWriteRepository,
        user_read_repository: UserReadRepository,
        country_read_repository: CountryReadRepository,
        founder_write_repository: CompanyFounderWriteRepository,
        company_read_repository: CompanyReadRepository,
    ):
        self._company_write_repository = company_write_repository
        self._user_read_repository = user_read_repository
        self._country_read_repository = country_read_repository
        self._founder_write_repository = founder_write_repository
        self._company_read_repository = company_read_repository

    def create(self, command: CompanyCreateCommand) -> Company:
        """
        :raises CountryNotFoundException:
        :raises UserNotFoundException:
        :raises BusinessNumberAlreadyExistsException:
        """
        search_result: list[Company] = self._company_read_repository.get_all(
            CompanyFilter(
                business_id=command.business_id,
            )
        )
        if search_result:
            raise BusinessNumberAlreadyExistsException("This business number is already exists.")
        countries: list[Country] = self._country_read_repository.get_all(CountryFilter(code=command.country_code))

        if not countries:
            raise CountryNotFoundException(f"A country with code = {command.country_code.value} not found.")
        country: Country = countries[0]

        self._user_read_repository.get_by_id(command.representative_id)  # check

        founder: CompanyFounder = self._founder_write_repository.create(command.founder_create_payload)
        logger.debug(f"founder = {repr(founder)}")

        logger.debug(f"{founder.id=}")
        return self._company_write_repository.create(
            CompanyCreatePayload(
                name=command.name,
                founder_id=Id(value=founder.id),
                representative_id=command.representative_id,
                country_id=Id(value=country.id),
                business_id=command.business_id,
                established_date=command.established_date,
                description=command.description,
            )
        )
