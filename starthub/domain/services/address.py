from domain.exceptions.geo.country import CountryNotFoundException
from domain.models.geo.address import Address
from domain.models.geo.country import Country
from domain.ports.service import AbstractDomainService
from domain.repositories.country import CountryReadRepository
from domain.repositories.geo.address import AddressWriteRepository
from domain.value_objects.common import Id
from domain.value_objects.filter import CountryFilter
from domain.value_objects.geo import AddressCreateCommand, AddressCreatePayload


class AddressService(AbstractDomainService):
    def __init__(
        self,
        write_repository: AddressWriteRepository,
        country_read_repositroy: CountryReadRepository,
    ):
        self._write_repository = write_repository
        self._country_read_repositroy = country_read_repositroy

    def create(self, command: AddressCreateCommand) -> Address:
        countries: list[Country] = self._country_read_repositroy.get_all(
            filter_=CountryFilter(code=command.country_code)
        )
        if not countries:
            raise CountryNotFoundException(f"Country with the code = {command.country_code.value} not found.")

        country: Country = countries[0]
        payload = self._convert_create_to_payload(command=command, country_id=Id(value=country.id))

        return self._write_repository.create(data=payload)

    def _convert_create_to_payload(self, command: AddressCreateCommand, country_id: Id) -> AddressCreatePayload:
        return AddressCreatePayload(
            country_id=country_id,
            region_id=command.region_id,
            city_id=command.city_id,
            district=command.district,
            street=command.street,
            house_number=command.house_number,
            postal_code=command.postal_code,
            raw_address=command.raw_address,
        )
