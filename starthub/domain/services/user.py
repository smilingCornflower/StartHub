from io import BytesIO

from domain.constants import PROFILE_PICTURE_PATH
from domain.exceptions.user import ProfilePictureNotFoundException
from domain.models.user import User
from domain.ports.cloud_storage import AbstractCloudStorage
from domain.repositories.user import UserReadRepository, UserWriteRepository
from domain.services.image import ImageService
from domain.value_objects.cloud_storage import CloudStorageCreateUrlPayload, CloudStorageUploadPayload
from domain.value_objects.common import FirstName, Id, LastName
from domain.value_objects.user import (
    Email,
    ProfilePictureUploadCommand,
    UserProfile,
    UserUpdateCommand,
    UserUpdatePayload,
)
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

    def update_user(self, command: UserUpdateCommand) -> None:
        """
        :raises UserNotFoundException:
        :raises NotSupportedImageFormat:
        """

        if command.picture_data:
            self.upload_profile_picture(
                ProfilePictureUploadCommand(
                    user_id=command.id_,
                    file_data=command.picture_data,
                )
            )
        self._user_write_repository.update(
            UserUpdatePayload(
                id_=command.id_,
                first_name=command.first_name,
                last_name=command.last_name,
                password=command.password,
            )
        )

    def upload_profile_picture(self, payload: ProfilePictureUploadCommand) -> None:
        """
        :raises UserNotFoundException:
        :raises NotSupportedImageFormatException: If image format is not in ("image/jpeg", "image/png", "image/gif", "image/webp", "image/avif").
        """
        converted_image_file: BytesIO = self._image_service.convert_to_jpg(BytesIO(payload.file_data))
        logger.info("The image converted to jpg successfully.")

        self._user_read_repository.get_by_id(payload.user_id)

        file_path = f"{PROFILE_PICTURE_PATH}/{payload.user_id.value}.jpg"
        logger.debug(f"file_path: {file_path}")

        uploaded_path: str = self._cloud_storage.upload_file(
            CloudStorageUploadPayload(file_data=converted_image_file.getvalue(), file_path=file_path)
        )
        logger.debug(f"File uploaded into the {uploaded_path}.")
        self._user_write_repository.update(UserUpdatePayload(id_=payload.user_id, picture=uploaded_path))
        logger.debug("user.picture field uploaded into the database.")

    def get_user_profile_picture(self, user_id: Id) -> str:
        """
        :raises UserNotFoundException:
        :raises ProfilePictureNotFoundException:
        """
        user: User = self._user_read_repository.get_by_id(user_id)
        if user.picture:
            return self._cloud_storage.create_url(payload=CloudStorageCreateUrlPayload(file_path=user.picture))
        raise ProfilePictureNotFoundException(f"The user with id = {user.id} does not have profile picture.")

    def get_user_profile(self, user_id: Id) -> UserProfile:
        """:raises UserNotFoundException:"""
        user: User = self._user_read_repository.get_by_id(user_id)

        picture_url: str | None = None

        if user.picture:
            picture_url = self._cloud_storage.create_url(payload=CloudStorageCreateUrlPayload(file_path=user.picture))

        return UserProfile(
            id_=Id(value=user.id),
            first_name=FirstName(value=user.first_name),
            last_name=LastName(value=user.last_name),
            email=Email(value=user.email),
            picture=picture_url,
        )
