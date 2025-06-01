from datetime import date

from domain.exceptions.validation import ValidationException
from domain.ports.payload import AbstractCreatePayload, AbstractUpdatePayload
from domain.validators.business_number import KZBusinessNumberValidator
from domain.value_objects import BaseVo
from domain.value_objects.common import Id
from domain.value_objects.country import CountryCode
from pydantic import field_validator
from pydantic_core.core_schema import ValidationInfo


class BusinessNumber(BaseVo):
    country_code: CountryCode
    value: str

    @field_validator("value", mode="after")
    @classmethod
    def is_correct_business_number(cls, value: str, info: ValidationInfo) -> str:
        """:raises ValidationException:"""
        if info.data.get("country_code") and info.data["country_code"].value == "KZ":
            KZBusinessNumberValidator.validate(value)
        return value


class CompanyCreatePayload(AbstractCreatePayload, BaseVo):
    name: str
    representative_id: Id
    country_id: Id
    business_id: BusinessNumber
    established_date: date
    description: str

    @field_validator("established_date", mode="after")
    @classmethod
    def established_not_in_future(cls, value: date) -> date:
        """:raises ValidationException:"""
        if value > date.today():
            raise ValidationException("company_establishment_date must not be in the future.")
        return value


class CompanyUpdatePayload(AbstractUpdatePayload):
    pass
