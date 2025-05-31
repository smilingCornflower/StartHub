from datetime import date
from typing import Any

from domain.exceptions.validation import ValidationException
from domain.value_objects.base import BaseVo
from domain.value_objects.common import Id
from domain.value_objects.country import CountryCode
from domain.value_objects.project import BusinessNumber
from pydantic import field_validator


class CompanyCreateDraft(BaseVo):
    name: str
    representative_id: Id
    country_code: CountryCode
    business_id: BusinessNumber
    established_date: date
    description: str

    @field_validator("established_date", mode="before")
    @classmethod
    def established_not_in_future(cls, value: Any) -> date:
        """
        :raises ValidationException:
        :raises ValueError:
        """

        if not isinstance(value, str):
            raise ValueError("value must be str.")

        value_date = date.fromisoformat(value)

        if value_date > date.today():
            raise ValidationException("company_establishment_date must not be in the future.")
        return value_date
