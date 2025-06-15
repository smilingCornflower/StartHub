import re
from datetime import date

import phonenumbers
from domain.constants import CHAR_FIELD_SHORT_LENGTH, DESCRIPTION_MAX_LENGTH
from domain.enums.social_links import SocialPlatform
from domain.exceptions.validation import (
    DeadlineInPastException,
    DisallowedSocialLinkException,
    EmptyStringException,
    FirstNameIsTooLongException,
    InvalidPhoneNumberException,
    InvalidSocialLinkException,
    LastNameIsTooLongException,
    StringIsTooLongException,
)
from domain.value_objects import BaseVo
from pydantic import ValidationInfo, field_validator


class Id(BaseVo):
    value: int


class Slug(BaseVo):
    value: str


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
