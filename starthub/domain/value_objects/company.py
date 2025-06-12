from datetime import date

from domain.constants import CHAR_FIELD_MAX_LENGTH
from domain.exceptions.company import CompanyNameIsTooLongException
from domain.exceptions.validation import DateInFutureException, EmptyStringException
from domain.ports.command import BaseCommand
from domain.ports.payload import AbstractCreatePayload, AbstractUpdatePayload
from domain.validators.business_number import KZBusinessNumberValidator
from domain.value_objects import BaseVo
from domain.value_objects.common import FirstName, Id, LastName
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


class CompanyFounderCreatePayload(AbstractCreatePayload, BaseVo):
    name: FirstName
    surname: LastName
    description: str | None


class CompanyFounderUpdatePayload(AbstractUpdatePayload, BaseVo):
    name: FirstName | None
    surname: LastName | None
    description: str | None


class CompanyCreatePayload(AbstractCreatePayload, BaseVo):
    name: str  # TODO: Company name is VO
    founder_id: Id
    representative_id: Id
    country_id: Id
    business_id: BusinessNumber
    established_date: date
    description: str


class CompanyUpdatePayload(AbstractUpdatePayload):
    project_id: Id
    name: str | None = None
    description: str | None = None
    established_date: date | None = None

    @field_validator("name", mode="after")
    @classmethod
    def is_valid_name(cls, value: str | None) -> str | None:
        """
        :raises CompanyNameIsTooLongException:
        :raises EmptyStringException:
        """
        if value is not None:
            if not value:
                raise EmptyStringException("Company name cannot be empty.")
            if len(value) > CHAR_FIELD_MAX_LENGTH:
                raise CompanyNameIsTooLongException(
                    f"Company name must be at most {CHAR_FIELD_MAX_LENGTH} characters long."
                )
        return value

    @field_validator("established_date", mode="after")
    @classmethod
    def established_not_in_future(cls, value: date | None) -> date | None:
        """:raises DateInFutureException:"""
        if value is not None:
            if value > date.today():
                raise DateInFutureException("company_establishment_date must not be in the future.")
        return value


class CompanyCreateCommand(BaseCommand):
    name: str
    representative_id: Id
    country_code: CountryCode
    business_id: BusinessNumber
    established_date: date
    founder_create_payload: CompanyFounderCreatePayload
    description: str

    @field_validator("established_date", mode="after")
    @classmethod
    def established_not_in_future(cls, value: date) -> date:
        """:raises DateInFutureException:"""
        if value > date.today():
            raise DateInFutureException("company_establishment_date must not be in the future.")
        return value

    @field_validator("name", mode="after")
    @classmethod
    def is_valid_name(cls, value: str) -> str:
        """
        :raises CompanyNameIsTooLongException:
        :raises EmptyStringException:
        """
        if not value:
            raise EmptyStringException("Company name cannot be empty.")
        if len(value) > CHAR_FIELD_MAX_LENGTH:
            raise CompanyNameIsTooLongException(
                f"Company name must be at most {CHAR_FIELD_MAX_LENGTH} characters long."
            )
        return value
