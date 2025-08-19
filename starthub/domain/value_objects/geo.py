from domain.ports.command import BaseCommand
from domain.ports.payload import AbstractCreatePayload, AbstractUpdatePayload
from domain.value_objects import BaseVo
from domain.value_objects.common import Id
from domain.value_objects.country import CountryCode, CountryId


class RegionId(Id):
    pass


class CityId(Id):
    pass


class AddressId(Id):
    pass


class RegionName(BaseVo):
    value: str


class CityName(BaseVo):
    value: str


class AddressVo(BaseVo):
    country_code: CountryCode
    region_id: RegionId
    city_id: CityId
    district: str | None = None
    street: str | None = None
    house_number: str | None = None
    postal_code: str | None = None

    raw_address: str | None = None


class AddressCreateCommand(BaseCommand):
    country_code: CountryCode
    region_id: RegionId
    city_id: CityId

    district: str | None = None
    street: str | None = None
    house_number: str | None = None
    postal_code: str | None = None

    raw_address: str | None = None


class AddressCreatePayload(AbstractCreatePayload):
    country_id: CountryId
    region_id: RegionId
    city_id: CityId

    district: str | None = None
    street: str | None = None
    house_number: str | None = None
    postal_code: str | None = None

    raw_address: str | None = None


class AddressUpdatePayload(AbstractUpdatePayload):
    pass


class RegionGetCommand(BaseCommand):
    all_languages: bool = False
