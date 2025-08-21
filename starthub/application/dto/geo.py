from dataclasses import dataclass

from domain.enums.language import LangCodeEnum


@dataclass(frozen=True)
class AddressDto:
    country_code: str
    region_name: str
    city_name: str

    district: str | None = None
    street: str | None = None
    house_number: str | None = None
    postal_code: str | None = None

    raw_address: str | None = None


type RegionNameAlias = str


@dataclass(frozen=True)
class RegionDto:
    id: int
    names: dict[LangCodeEnum, RegionNameAlias]


type CityNameAlias = str


@dataclass(frozen=True)
class CityDto:
    id: int
    names: dict[LangCodeEnum, CityNameAlias]
