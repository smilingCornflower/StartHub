from application.converters.request_converters.user import request_files_to_profile_picture_bytes
from application.ports.service import AbstractAppService
from django.core.files.uploadedfile import UploadedFile
from domain.services.user import UserService
from domain.value_objects.common import Id
from domain.value_objects.user import ProfilePictureUploadPayload
from loguru import logger


class UserAppService(AbstractAppService):
    def __init__(self, user_service: UserService):
        self._user_service = user_service

    def upload_profile_picture(self, request_files: dict[str, UploadedFile], user_id: int) -> None:
        image_data: bytes = request_files_to_profile_picture_bytes(request_files)
        self._user_service.upload_profile_picture(
            ProfilePictureUploadPayload(
                user_id=Id(value=user_id),
                file_data=image_data,
            )
        )
        logger.info("Profile picture uploaded successfully.")
