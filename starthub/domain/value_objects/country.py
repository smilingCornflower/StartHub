import pycountry
from domain.exceptions.geo.country import InvalidCountryCodeException
from domain.value_objects import BaseVo
from domain.value_objects.common import Id
from pydantic import field_validator


class CountryId(Id):
    pass


class CountryCode(BaseVo):
    value: str

    @field_validator("value", mode="after")
    @classmethod
    def is_correct_country_code(cls, value: str) -> str:
        """:raises InvalidCountryCodeException:"""
        if not value.isupper():
            raise InvalidCountryCodeException("Country code must be uppercase ISO alpha-2")
        if pycountry.countries.get(alpha_2=value) is None:
            raise InvalidCountryCodeException(f"Invalid country code: {value}")
        return value
