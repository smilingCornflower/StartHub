from typing import Any

from django.core.files.uploadedfile import UploadedFile
from domain.value_objects.common import Description, FirstName, Id, LastName, PhoneNumber
from domain.value_objects.user import RawPassword, UserUpdateCommand
from loguru import logger


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
