import re
from dataclasses import dataclass

from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from domain.constants import (
    PASSWORD_MAX_LENGTH,
    PASSWORD_MIN_LENGTH,
    PASSWORD_PATTERN,
    USERNAME_MAX_LENGTH,
    USERNAME_MIN_LENGTH,
    USERNAME_PATTERN,
)
from domain.exceptions.validation import ValidationException
from domain.ports.payload import AbstractCreatePayload, AbstractUpdatePayload
from domain.value_objects.common import Id


@dataclass(frozen=True)
class Username:
    value: str

    def __post_init__(self) -> None:
        if not isinstance(self.value, str):
            raise TypeError("Username value must be str.")
        if not (USERNAME_MIN_LENGTH <= len(self.value) <= USERNAME_MAX_LENGTH):
            raise ValidationException(f"Username must be {USERNAME_MIN_LENGTH}-{USERNAME_MAX_LENGTH} chars.")
        if not re.match(USERNAME_PATTERN, self.value):
            raise ValidationException("Username contains invalid characters.")


@dataclass(frozen=True)
class RawPassword:
    value: str

    def __post_init__(self) -> None:
        if not isinstance(self.value, str):
            raise TypeError("RawPassword value must be str.")
        if not (PASSWORD_MIN_LENGTH <= len(self.value) <= PASSWORD_MAX_LENGTH):
            raise ValidationException(f"Password must be {PASSWORD_MIN_LENGTH}-{PASSWORD_MAX_LENGTH} chars.")
        if not re.match(PASSWORD_PATTERN, self.value):
            raise ValidationException(
                "Password must contain at least one digit, one uppercase letter and one lowercase letter."
            )


@dataclass(frozen=True)
class Email:
    value: str

    def __post_init__(self) -> None:
        if not isinstance(self.value, str):
            raise TypeError("Email value must be str.")
        email_validator = EmailValidator()
        try:
            email_validator(self.value)
        except ValidationError:
            raise ValidationException(f"Invalid email address: {self.value}.")


@dataclass(frozen=True)
class UserCreatePayload(AbstractCreatePayload):
    username: Username
    email: Email
    password: RawPassword


@dataclass(frozen=True)
class UserUpdatePayload(AbstractUpdatePayload):
    id_: Id
    username: Username | None = None
    email: Email | None = None
    password: RawPassword | None = None
