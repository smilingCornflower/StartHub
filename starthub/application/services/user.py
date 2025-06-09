from typing import Any

from application.converters.request_converters.user import request_to_user_update_command
from application.converters.resposne_converters.user import user_profile_to_dto
from application.dto.user import UserProfileDto
from application.ports.service import AbstractAppService
from django.core.files.uploadedfile import UploadedFile
from domain.services.user import UserService
from domain.value_objects.common import Id
from domain.value_objects.user import UserProfile, UserUpdateCommand
from loguru import logger


class UserAppService(AbstractAppService):
    def __init__(self, user_service: UserService):
        self._user_service = user_service

    def update_user(self, request_data: dict[str, Any], request_files: dict[str, UploadedFile], user_id: int) -> None:
        """
        :raises FirstNameIsTooLongException:
        :raises LastNameIsTooLongException:
        :raises EmptyStringException:
        :raises pydantic.ValidationError:
        :raises PasswordValidationException:
        :raises UserNotFoundException:
        :raises NotSupportedImageFormat:
        """
        command: UserUpdateCommand = request_to_user_update_command(request_data, request_files, user_id=user_id)
        logger.warning("Started user updating.")

        self._user_service.update_user(command)
        logger.info("User updated successfully.")

    def get_user_profile(self, user_id: int) -> UserProfileDto:
        """:raises UserNotFoundException:"""
        user_profile: UserProfile = self._user_service.get_user_profile(user_id=Id(value=user_id))
        return user_profile_to_dto(user_profile)

    def get_user_own_profile(self, user_id: int) -> UserProfileDto:
        """:raises UserNotFoundException:"""
        user_profile: UserProfile = self._user_service.get_user_profile(user_id=Id(value=user_id))
        return user_profile_to_dto(user_profile)
