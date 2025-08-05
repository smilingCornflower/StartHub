from dataclasses import dataclass


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
