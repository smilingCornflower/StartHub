import re

from django.core.exceptions import ValidationError as DjValidationError
from django.core.validators import EmailValidator
from domain.constants import PASSWORD_MAX_LENGTH, PASSWORD_MIN_LENGTH, PASSWORD_PATTERN
from domain.exceptions.auth import PasswordValidationException
from domain.exceptions.validation import EmptyStringException, InvalidEmailException
from domain.ports.payload import AbstractCreatePayload, AbstractUpdatePayload
from domain.value_objects import BaseVo
from domain.value_objects.common import FirstName, Id, LastName
from pydantic import field_validator


class RawPassword(BaseVo):
    value: str

    @field_validator("value", mode="after")
    @classmethod
    def is_strong_password(cls, value: str) -> str:
        if not value:
            raise EmptyStringException("Password cannot be empty.")

        if not (PASSWORD_MIN_LENGTH <= len(value) <= PASSWORD_MAX_LENGTH):
            raise PasswordValidationException(f"Password must be {PASSWORD_MIN_LENGTH}-{PASSWORD_MAX_LENGTH} chars.")

        if not re.match(PASSWORD_PATTERN, value):
            raise PasswordValidationException(
                "Password must contain at least one digit, one uppercase letter and one lowercase letter."
            )
        return value


class Email(BaseVo):
    value: str

    @field_validator("value", mode="after")
    @classmethod
    def is_valid_email(cls, value: str) -> str:
        if not value:
            raise EmptyStringException("Email cannot be empty.")
        email_validator = EmailValidator()
        try:
            email_validator(value)
        except DjValidationError:
            raise InvalidEmailException(f"Invalid email address: {value}.")
        return value


class UserCreatePayload(AbstractCreatePayload):
    first_name: FirstName
    last_name: LastName
    email: Email
    password: RawPassword


class UserUpdatePayload(AbstractUpdatePayload):
    id_: Id
    first_name: FirstName | None = None
    last_name: LastName | None = None
    email: Email | None = None
    password: RawPassword | None = None
    picture: str | None = None


class ProfilePictureUploadPayload(AbstractCreatePayload):
    user_id: Id
    file_data: bytes
