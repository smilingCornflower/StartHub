from datetime import date

from domain.exceptions.validation import ValidationException
from domain.ports.payload import AbstractCreatePayload, AbstractUpdatePayload
from domain.value_objects.base import BaseVo
from domain.value_objects.common import Id
from domain.value_objects.project import BusinessNumber
from pydantic import field_validator


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
