from datetime import date
from typing import Any

from domain.exceptions.validation import ValidationException
from domain.value_objects import BaseVo
from domain.value_objects.common import Id
from domain.value_objects.company import BusinessNumber
from domain.value_objects.country import CountryCode
from pydantic import field_validator


# TODO: Use Command instead of Draft
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
