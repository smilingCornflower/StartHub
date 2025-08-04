from domain.ports.command import BaseCommand
from domain.ports.payload import AbstractCreatePayload, AbstractUpdatePayload
from domain.value_objects import BaseVo
from domain.value_objects.common import CountryCode, Id


class RegionName(BaseVo):
    value: str


class CityName(BaseVo):
    value: str


class AddressVo(BaseVo):
    country_code: CountryCode
    region: RegionName
    city: CityName
    district: str | None = None
    street: str | None = None
    house_number: str | None = None
    postal_code: str | None = None

    raw_address: str | None = None


class AddressCreateCommand(BaseCommand):
    country_code: CountryCode
    region_id: Id
    city_id: Id

    district: str | None = None
    street: str | None = None
    house_number: str | None = None
    postal_code: str | None = None

    raw_address: str | None = None


class AddressCreatePayload(AbstractCreatePayload):
    country_id: Id
    region_id: Id
    city_id: Id

    district: str | None = None
    street: str | None = None
    house_number: str | None = None
    postal_code: str | None = None

    raw_address: str | None = None


class AddressUpdatePayload(AbstractUpdatePayload):
    pass
