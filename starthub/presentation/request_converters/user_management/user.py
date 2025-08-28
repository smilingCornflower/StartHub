from typing import Any, cast

from django.core.files.uploadedfile import UploadedFile
from django.http import QueryDict
from domain.exceptions.validation import ValidationException
from domain.value_objects.common import Description, FirstName, Id, LastName, PhoneNumber
from domain.value_objects.user_management.user import Email, RawPassword, UserGetCommand, UserUpdateCommand
from loguru import logger
from presentation.request_converters.common import get_role_if_exists_from_params, parse_date
from rest_framework.request import Request


def request_to_user_update_command(
    data: dict[str, Any], files: dict[str, UploadedFile], user_id: int
) -> UserUpdateCommand:
    """
    :raises FirstNameIsTooLongException:
    :raises LastNameIsTooLongException:
    :raises EmptyStringException:
    :raises pydantic.ValidationError:
    :raises PasswordValidationException:
    :raises InvalidPhoneNumberException:
    """
    image_file: UploadedFile | None = files.get("profile_picture")
    first_name: Any | None = data.get("first_name")
    last_name: Any | None = data.get("last_name")
    password: Any | None = data.get("password")
    description: Any | None = data.get("description")
    add_phone: Any | None = data.get("add_phone")
    remove_phone: Any | None = data.get("remove_phone")

    result = UserUpdateCommand(user_id=Id(value=user_id))

    if image_file is not None:
        logger.info("Image file is provided.")
        result.picture_data = image_file.read()
    if first_name is not None:
        logger.info("first_name is provided.")
        result.first_name = FirstName(value=first_name)
    if last_name is not None:
        logger.info("last_name is provided.")
        result.last_name = LastName(value=last_name)
    if password is not None:
        logger.info("password is provided.")
        result.password = RawPassword(value=password)
    if description is not None:
        logger.info("description is provided.")
        result.description = Description(value=description)
    if add_phone is not None:
        logger.info("add_phone is provided.")
        result.add_phone = PhoneNumber(value=add_phone)
    if remove_phone is not None:
        logger.info("remove_phone is provided.")
        result.remove_phone = PhoneNumber(value=remove_phone)

    return result


# ==== UserGetCommand ====
def get_is_active_if_exists_from_params(params: QueryDict) -> bool | None:
    """:raises ValidationException:"""
    if params.get("is_active"):
        if params["is_active"] == "true":
            return True
        elif params["is_active"] == "false":
            return False
        else:
            raise ValidationException(
                f"Invalid value for is_active: {params['is_active']}. Expected: 'true' or 'false'."
            )
    else:
        return None


def request_to_user_get_command(request: Request) -> UserGetCommand:
    params: QueryDict = request.query_params
    command = UserGetCommand(
        role=get_role_if_exists_from_params(params=params),
        is_active=get_is_active_if_exists_from_params(params=params),
        email=Email(value=cast(str, params["email"])) if "email" in params else None,
        first_name=FirstName(value=cast(str, params["first_name"])) if "first_name" in params else None,
        last_name=LastName(value=cast(str, params["last_name"])) if "last_name" in params else None,
        date_joined_start=parse_date(cast(str, params["date_joined_start"])) if "date_joined_start" in params else None,
        date_joined_end=parse_date(cast(str, params["date_joined_end"])) if "date_joined_end" in params else None,
    )
    logger.debug(f"command = {command}")
    return command
