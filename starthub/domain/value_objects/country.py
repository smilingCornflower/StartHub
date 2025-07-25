from domain.exceptions.country import InvalidCountryCodeException
from domain.value_objects import BaseVo
from pydantic import field_validator


class CountryCode(BaseVo):
    value: str

    @field_validator("value", mode="after")
    @classmethod
    def is_correct_country_code(cls, value: str) -> str:
        """:raises InvalidCountryCodeException:"""
        if not (len(value) == 2 and value.isalpha() and value.isupper()):
            raise InvalidCountryCodeException("Invalid country code")
        return value
