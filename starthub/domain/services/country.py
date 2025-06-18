from domain.exceptions.country import CountryNotFoundException
from domain.models.country import Country
from domain.ports.service import AbstractDomainService
from domain.repositories.country import CountryReadRepository
from domain.value_objects.country import CountryCode
from domain.value_objects.filter import CountryFilter


class CountryService(AbstractDomainService):
    def __init__(self, country_read_repository: CountryReadRepository):
        self._country_read_repository = country_read_repository

    def get_country_by_code(self, code: CountryCode) -> Country:
        """
        :raises CountryNotFoundException:
        """
        country: list[Country] = self._country_read_repository.get_all(
            CountryFilter(code=CountryCode(value=code.value))
        )
        if not country:
            raise CountryNotFoundException(f"Country with code = {code} not found.")
        return country[0]
