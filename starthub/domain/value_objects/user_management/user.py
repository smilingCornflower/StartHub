import re
from datetime import date

from django.core.exceptions import ValidationError as DjValidationError
from django.core.validators import EmailValidator
from domain.constants import PASSWORD_MAX_LENGTH, PASSWORD_MIN_LENGTH, PASSWORD_PATTERN
from domain.enums.permission import ActionEnum, ScopeEnum
from domain.enums.role import RoleEnum
from domain.exceptions.auth import PasswordValidationException
from domain.exceptions.validation import EmptyStringException, InvalidEmailException
from domain.models.role import Role
from domain.ports.command import BaseCommand
from domain.ports.payload import AbstractCreatePayload, AbstractUpdatePayload
from domain.value_objects import BaseVo
from domain.value_objects.common import Description, FirstName, Id, LastName, PhoneNumber
from pydantic import field_validator


class RawPassword(BaseVo):
    value: str

    @field_validator("value", mode="after")
    @classmethod
    def validate_password(cls, value: str) -> str:
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
    def validate_email(cls, value: str) -> str:
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
    description: Description | None = None
    password: RawPassword | None = None
    picture: str | None = None

    is_active: bool | None = None
    role_to_add: Role | None = None
    role_to_remove: Role | None = None


class ProfilePictureUploadCommand(BaseCommand):
    user_id: Id
    file_data: bytes


class UserProfile(BaseVo):
    id_: Id
    first_name: FirstName
    last_name: LastName
    description: Description
    email: Email
    picture: str | None
    phone_numbers: list[PhoneNumber]


# Commands
class UserUpdateCommand(BaseCommand):
    user_id: Id
    first_name: FirstName | None = None
    last_name: LastName | None = None
    description: Description | None = None
    password: RawPassword | None = None
    picture_data: bytes | None = None
    add_phone: PhoneNumber | None = None
    remove_phone: PhoneNumber | None = None


class PermissionVo(BaseVo):
    value: str

    @field_validator("value", mode="after")
    @classmethod
    def validate_permission(cls, value: str) -> str:
        """
        Validation format of permission string:
        - action.scope.model
        - action.scope.model.field
        - action.scope.model.field.value
        """
        parts: list[str] = value.split(".")

        if len(parts) not in (3, 4, 5):
            raise ValueError(
                "Permission must be in format 'action.scope.model', "
                "'action.scope.model.field', or 'action.scope.model.field.value'"
            )
        field = None
        if len(parts) == 3:
            action, scope, model = parts
        elif len(parts) == 4:
            action, scope, model, field = parts
        else:
            action, scope, model, field, fiel_value = parts

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
            if not field.isidentifier() or not field.islower():
                raise ValueError("Field name must be lowercase and valid Python identifier")

        return value


class UserPhoneCreatePayload(AbstractCreatePayload):
    user_id: Id
    phone: PhoneNumber


class UserPhoneUpdatePayload(AbstractUpdatePayload):
    pass


class UserGetCommand(BaseCommand):
    role: RoleEnum | None
    is_active: bool | None
    email: Email | None
    first_name: FirstName | None
    last_name: LastName | None
    date_joined_start: date | None
    date_joined_end: date | None
