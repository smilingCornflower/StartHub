from io import BytesIO

from domain.constants import PROFILE_PICTURE_PATH
from domain.exceptions.user import ProfilePictureNotFoundException
from domain.models.user import User
from domain.ports.cloud_storage import AbstractCloudStorage
from domain.repositories.user import UserReadRepository, UserWriteRepository
from domain.services.image import ImageService
from domain.value_objects.cloud_storage import (
    CloudStorageCreateUrlPayload,
    CloudStorageDeletePayload,
    CloudStorageUploadPayload,
)
from domain.value_objects.common import Id
from domain.value_objects.user import ProfilePictureUploadPayload, UserUpdatePayload
from loguru import logger


class UserService:
    def __init__(
        self,
        cloud_storage: AbstractCloudStorage,
        user_read_repository: UserReadRepository,
        user_write_repository: UserWriteRepository,
        image_service: ImageService,
    ):
        self._cloud_storage = cloud_storage
        self._user_read_repository = user_read_repository
        self._user_write_repository = user_write_repository
        self._image_service = image_service

    def upload_profile_picture(self, payload: ProfilePictureUploadPayload) -> None:
        """
        :raises UserNotFoundException:
        :raises InvalidImageException: If file appears incorrect image.
        :raises NotSupportedImageFormatException: If image formats are not in ('jpeg', 'png', 'webp').
        """

        converted_image_file: BytesIO = self._image_service.convert_to_jpg(BytesIO(payload.file_data))
        logger.info("The image converted to jpg successfully.")

        user: User = self._user_read_repository.get_by_id(payload.user_id)

        if user.picture:
            logger.info(f"Deleting previous profile picture: {user.picture}")
            self._cloud_storage.delete_file(CloudStorageDeletePayload(file_path=user.picture))

        file_path = f"{PROFILE_PICTURE_PATH}/{payload.user_id.value}.jpg"
        logger.debug(f"file_path: {file_path}")

        uploaded_path: str = self._cloud_storage.upload_file(
            CloudStorageUploadPayload(file_data=converted_image_file.getvalue(), file_path=file_path)
        )
        assert file_path == uploaded_path, "Expected and uploaded paths don`t match."

        logger.debug("Updating user.picture field.")
        self._user_write_repository.update(UserUpdatePayload(id_=payload.user_id, picture=uploaded_path))

    def get_user_profile_picture(self, user_id: Id) -> str:
        """
        :raises UserNotFoundException:
        :raises ProfilePictureNotFoundException:
        """
        user: User = self._user_read_repository.get_by_id(user_id)
        if user.picture:
            return self._cloud_storage.create_url(payload=CloudStorageCreateUrlPayload(file_path=user.picture))
        raise ProfilePictureNotFoundException(f"The user with id = {user.id} does not have profile picture.")
