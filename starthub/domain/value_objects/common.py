import re
import uuid
from datetime import date
from typing import ClassVar

import phonenumbers
from domain.constants import (
    CHAR_FIELD_MAX_LENGTH,
    CHAR_FIELD_MEDIUM_LENGTH,
    CHAR_FIELD_SHORT_LENGTH,
    DESCRIPTION_MAX_LENGTH,
    PAGINNATION_MAX_LMIT,
)
from domain.enums.social_links import SocialPlatform
from domain.exceptions import CustomException
from domain.exceptions.pagination import PaginationMaxLimitException
from domain.exceptions.validation import (
    DeadlineInPastException,
    DisallowedSocialLinkException,
    EmptyStringException,
    FirstNameIsTooLongException,
    InvalidPhoneNumberException,
    InvalidSocialLinkException,
    LastNameIsTooLongException,
    NegativeNumberException,
    StringIsTooLongException,
)
from domain.value_objects import BaseVo
from pydantic import Field, ValidationInfo, field_validator


class Id(BaseVo):
    value: int

    def __int__(self) -> int:
        return self.value


class Uuid(BaseVo):
    value: str = Field(default_factory=lambda: str(uuid.uuid4()))


class Slug(BaseVo):
    value: str


class StringVo(BaseVo):
    value: str

    empty_string_exception: ClassVar[type[CustomException]] = EmptyStringException
    too_long_string_exception: ClassVar[type[CustomException]] = StringIsTooLongException
    max_length: ClassVar[int | None] = None

    @classmethod
    def get_empty_string_msg(cls) -> str:
        return "String cannot be empty."

    @classmethod
    def get_too_long_string_msg(cls) -> str:
        if cls.max_length:
            return f"String must be no longer than {cls.max_length} characters."
        return "String is too long."

    @field_validator("value", mode="after")
    @classmethod
    def validate_string(cls, value: str) -> str:
        if not value.strip():
            msg = cls.get_empty_string_msg()
            raise cls.empty_string_exception(msg)

        if cls.max_length and len(value) > cls.max_length:
            msg = cls.get_too_long_string_msg()
            raise cls.too_long_string_exception(msg)

        return value


class MediumString(StringVo):
    max_length: ClassVar[int] = CHAR_FIELD_MEDIUM_LENGTH


class LongString(BaseVo):
    value: str

    @field_validator("value", mode="after")
    @classmethod
    def validate_length(cls, value: str) -> str:
        if not value.strip():
            raise EmptyStringException("First name cannot be empty.")
        if len(value) > CHAR_FIELD_MAX_LENGTH:
            raise StringIsTooLongException(f"String must be no longer than {CHAR_FIELD_MAX_LENGTH} characters.")
        return value


class PositiveNumber(BaseVo):
    value: float

    @field_validator("value", mode="after")
    @classmethod
    def validate_positive_number(cls, value: float) -> float:
        """:raises NegativeNumberException:"""
        if value < 0:
            raise NegativeNumberException("Value must be positive.")
        return value


class FirstName(BaseVo):
    value: str

    @field_validator("value", mode="after")
    @classmethod
    def validate_length(cls, value: str) -> str:
        if not value.strip():
            raise EmptyStringException("First name cannot be empty.")
        if len(value) > CHAR_FIELD_SHORT_LENGTH:
            raise FirstNameIsTooLongException(
                f"First name must be no longer than {CHAR_FIELD_SHORT_LENGTH} characters."
            )
        return value.strip()


class LastName(BaseVo):
    value: str

    @field_validator("value", mode="after")
    @classmethod
    def validate_length(cls, value: str) -> str:
        """
        :raises EmptyStringException:
        :raises LastNameIsTooLongException:
        """
        if not value.strip():
            raise EmptyStringException("Last name cannot be empty.")
        if len(value) > CHAR_FIELD_SHORT_LENGTH:
            raise LastNameIsTooLongException(f"Last name must be no longer than {CHAR_FIELD_SHORT_LENGTH} characters")
        return value.strip()


class PhoneNumber(BaseVo):
    value: str

    @field_validator("value", mode="after")
    @classmethod
    def is_correct_phone_number(cls, value: str) -> str:
        """:raises InvalidPhoneNumberException:"""
        try:
            parsed: phonenumbers.PhoneNumber = phonenumbers.parse(value)
        except phonenumbers.NumberParseException:
            raise InvalidPhoneNumberException(f"Invalid phone number: {value}")

        if not phonenumbers.is_valid_number(parsed):
            raise InvalidPhoneNumberException(f"Invalid phone number: {value}")

        return phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)


class SocialLink(BaseVo):
    platform: str
    link: str

    @field_validator("link", mode="after")
    @classmethod
    def validate_social_link(cls, value: str, info: ValidationInfo) -> str:
        """
        :raises DisallowedSocialLinkException:
        :raises InvalidSocialLinkException:
        """
        try:
            platform = SocialPlatform(info.data["platform"])
        except ValueError:
            raise DisallowedSocialLinkException(f"Unknown social platform: {info.data["platform"]}")
        if not re.match(platform.pattern, value):
            raise InvalidSocialLinkException(f"Invalid link for platform {platform.value}")
        return value


class DeadlineDate(BaseVo):
    value: date

    @field_validator("value", mode="after")
    @classmethod
    def validate_deadline_not_in_past(cls, value: date) -> date:
        """:raises DeadlineInPastException:"""
        if value <= date.today():
            raise DeadlineInPastException("deadline must be in the future.")
        return value


class Description(BaseVo):
    value: str

    @field_validator("value", mode="after")
    @classmethod
    def validate_description_length(cls, value: str) -> str:
        """:raises StringIsTooLongException:"""
        if len(value) > DESCRIPTION_MAX_LENGTH:
            raise StringIsTooLongException(
                f"Description is too long. Max length is {DESCRIPTION_MAX_LENGTH} characters."
            )
        return value


class Order(BaseVo):
    value: int


class Pagination(BaseVo):
    last_id: int | None = None
    limit: int

    @field_validator("limit", mode="after")
    @classmethod
    def validate_limit_max_value(cls, limit: int) -> int:
        """:raises PaginationMaxLimitException:"""
        if limit > PAGINNATION_MAX_LMIT:
            raise PaginationMaxLimitException(f"limit must not exceed {PAGINNATION_MAX_LMIT}.")
        return limit


class OffsetPagination(BaseVo):
    offset: int = 0
    limit: int
