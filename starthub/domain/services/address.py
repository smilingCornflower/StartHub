from domain.exceptions.geo.geo import GeographicalInconsistencyException
from domain.models import City
from domain.models.geo.address import Address
from domain.models.geo.country import Country
from domain.ports.service import AbstractDomainService
from domain.repositories.country import CountryReadRepository
from domain.repositories.geo.address import AddressReadRepository, AddressWriteRepository
from domain.repositories.geo.city import CityReadRepository
from domain.services.permission import PermissionService
from domain.value_objects.country import CountryId
from domain.value_objects.filter import AddressFilter
from domain.value_objects.geo import AddressCreateCommand, AddressCreatePayload, CityId, RegionId
from loguru import logger


class AddressService(AbstractDomainService):
    def __init__(
        self,
        read_repository: AddressReadRepository,
        write_repository: AddressWriteRepository,
        country_read_repositroy: CountryReadRepository,
        city_read_repository: CityReadRepository,
        permission_service: PermissionService,
    ):
        self._read_repository = read_repository
        self._write_repository = write_repository
        self._country_read_repositroy = country_read_repositroy
        self._city_read_repository = city_read_repository
        self._permission_service = permission_service

    def create(self, command: AddressCreateCommand) -> Address:
        """
        :raises CountryNotFoundException:
        :raises CityNotFoundException:
        :raises GeographicalInconsistencyException:
        """

        duplicate_address: Address | None = self._get_duplicate_address_or_none(command=command)
        if duplicate_address is not None:
            logger.debug("Duplicate address found, returning existing address.")
            return duplicate_address

        self._check_city_in_region(region_id=command.region_id, city_id=command.city_id)
        country: Country = self._country_read_repositroy.get_by_code(code=command.country_code)
        payload = self._convert_create_to_payload(command=command, country_id=CountryId(value=country.id))

        address: Address = self._write_repository.create(data=payload)
        logger.info("Address created.")
        return address

    def _get_duplicate_address_or_none(self, command: AddressCreateCommand) -> Address | None:
        """:raises CountryNotFoundException:"""
        country_id: CountryId | None = None
        if command.country_code:
            country: Country = self._country_read_repositroy.get_by_code(code=command.country_code)
            country_id = CountryId(value=country.id)

        adresses: list[Address] = self._read_repository.get_all(
            filter_=AddressFilter(
                country_id=country_id,
                region_id=command.region_id,
                city_id=command.city_id,
                district=command.district,
                street=command.street,
                house_number=command.house_number,
                postal_code=command.postal_code,
                raw_address=command.raw_address,
            )
        )
        if adresses:
            return adresses[0]

        return None

    def _check_city_in_region(self, region_id: RegionId, city_id: CityId) -> None:
        """
        :raises CityNotFoundException:
        :raises GeographicalInconsistencyException:
        """
        city: City = self._city_read_repository.get_by_id(id_=city_id)

        if city.region.id != region_id.value:
            logger.exception(f"City with id '{city_id.value}' does not belong to region with id {region_id.value}.")
            raise GeographicalInconsistencyException(
                f"City with id '{city_id.value}' does not belong to region with id {region_id.value}."
            )
        logger.debug(f"City with id '{city_id.value}' belongs to region with id {region_id.value}.")

    def _convert_create_to_payload(self, command: AddressCreateCommand, country_id: CountryId) -> AddressCreatePayload:
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
