import re

import phonenumbers
from domain.constants import CHAR_FIELD_SHORT_LENGTH
from domain.enums.social_links import SocialPlatform
from domain.exceptions.validation import (
    DisallowedSocialLinkException,
    EmptyStringException,
    FirstNameIsTooLongException,
    InvalidPhoneNumberException,
    InvalidSocialLinkException,
    LastNameIsTooLongException,
)
from domain.value_objects.base import BaseVo
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
        """:raises InvalidPhoneNumberValidationException:"""
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
        try:
            platform = SocialPlatform(info.data["platform"])
        except ValueError:
            raise DisallowedSocialLinkException(f"Unknown social platform: {info.data["platform"]}")
        if not re.match(platform.pattern, value):
            raise InvalidSocialLinkException(f"Invalid link for platform {platform.value}")
        return value
