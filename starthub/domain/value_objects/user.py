import re

from django.core.exceptions import ValidationError as DjValidationError
from django.core.validators import EmailValidator
from domain.constants import PASSWORD_MAX_LENGTH, PASSWORD_MIN_LENGTH, PASSWORD_PATTERN
from domain.enums.permission import ActionEnum, ScopeEnum
from domain.exceptions.auth import PasswordValidationException
from domain.exceptions.validation import EmptyStringException, InvalidEmailException
from domain.ports.command import BaseCommand
from domain.ports.payload import AbstractCreatePayload, AbstractUpdatePayload
from domain.value_objects import BaseVo
from domain.value_objects.common import FirstName, Id, LastName
from pydantic import field_validator


class RawPassword(BaseVo):
    value: str

    @field_validator("value", mode="after")
    @classmethod
    def is_strong_password(cls, value: str) -> str:
        """
        :raises EmptyStringException:
        :raises PasswordValidationException:
        """
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
        """
        :raises EmptyStringException:
        :raises InvalidEmailException:
        """
        if not value:
            raise EmptyStringException("Email cannot be empty.")
        email_validator = EmailValidator()
        try:
            email_validator(value)
        except DjValidationError:
            raise InvalidEmailException(f"Invalid email address: {value}.")
        return value


class UserCreatePayload(AbstractCreatePayload):
    email: Email
    password: RawPassword


class UserUpdatePayload(AbstractUpdatePayload):
    id_: Id
    first_name: FirstName | None = None
    last_name: LastName | None = None
    password: RawPassword | None = None
    picture: str | None = None


class ProfilePictureUploadCommand(BaseCommand):
    user_id: Id
    file_data: bytes


class UserProfile(BaseVo):
    id_: Id
    first_name: FirstName
    last_name: LastName
    email: Email
    picture: str | None


# Commands
class UserUpdateCommand(BaseCommand):
    id_: Id
    first_name: FirstName | None = None
    last_name: LastName | None = None
    password: RawPassword | None = None
    picture_data: bytes | None = None


class PermissionVo(BaseVo):
    value: str

    @field_validator("value", mode="after")
    @classmethod
    def validate_permission(cls, value: str) -> str:
        """
        Validation format of permission string:
        - action.scope.model.field
        - action.scope.model
        """
        parts: list[str] = value.split(".")

        if len(parts) not in (3, 4):
            raise ValueError("Permission must be in format 'action.scope.model' or 'action.scope.model.field'")

        action, scope, model, *field = parts

        try:
            ActionEnum(action)
        except ValueError:
            raise ValueError(f"Invalid action '{action}'. Must be one of: {', '.join(ActionEnum)}")

        try:
            ScopeEnum(scope)
        except ValueError:
            raise ValueError(f"Invalid scope '{scope}'. Must be one of: {', '.join(list(ScopeEnum))}")

        if not model.isidentifier() or not model.islower():
            raise ValueError("Model name must be lowercase and valid Python identifier")

        if field:
            field_name = field[0]
            if not field_name.isidentifier() or not field_name.islower():
                raise ValueError("Field name must be lowercase and valid Python identifier")

        return value
