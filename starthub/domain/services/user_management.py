from io import BytesIO

from domain.exceptions.user import ProfilePictureNotFoundException
from domain.exceptions.user_favorite import UserFavoriteAlreadyExistsException
from domain.models.user import User
from domain.models.user_favorite import UserFavorite
from domain.ports.cloud_storage import AbstractCloudStorage
from domain.ports.service import AbstractDomainService
from domain.repositories.project_management import ProjectReadRepository
from domain.repositories.user import UserReadRepository, UserWriteRepository
from domain.repositories.user_favorite import UserFavoriteReadRepository, UserFavoriteWriteRepository
from domain.services.file import ImageService
from domain.utils.path_provider import PathProvider
from domain.value_objects.cloud_storage import CloudStorageCreateUrlPayload, CloudStorageUploadPayload
from domain.value_objects.common import FirstName, Id, LastName, Description
from domain.value_objects.filter import UserFavoriteFilter
from domain.value_objects.user import (
    Email,
    ProfilePictureUploadCommand,
    UserProfile,
    UserUpdateCommand,
    UserUpdatePayload,
)
from domain.value_objects.user_favorite import UserFavoriteCreatePayload
from loguru import logger


class UserService(AbstractDomainService):
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
                description=command.description,
                password=command.password,
            )
        )

    def upload_profile_picture(self, command: ProfilePictureUploadCommand) -> None:
        """
        :raises UserNotFoundException:
        :raises NotSupportedImageFormatException: If image format is not in ("image/jpeg", "image/png", "image/gif", "image/webp", "image/avif").
        """
        converted_image_file: BytesIO = self._image_service.convert_to_jpg(BytesIO(command.file_data))
        logger.info("The image converted to jpg successfully.")

        self._user_read_repository.get_by_id(command.user_id)

        file_path = PathProvider.get_user_profile_picture_path(user_id=command.user_id)
        logger.debug(f"file_path: {file_path}")

        uploaded_path: str = self._cloud_storage.upload_file(
            CloudStorageUploadPayload(file_data=converted_image_file.getvalue(), file_path=file_path)
        )
        logger.debug(f"File uploaded into the {uploaded_path}.")
        self._user_write_repository.update(UserUpdatePayload(id_=command.user_id, picture=uploaded_path))
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
            description=Description(value=user.description),
            email=Email(value=user.email),
            picture=picture_url,
        )


class UserFavoriteService(AbstractDomainService):
    def __init__(
        self,
        user_favorite_read_repository: UserFavoriteReadRepository,
        user_favorite_write_repository: UserFavoriteWriteRepository,
        user_read_repository: UserReadRepository,
        project_read_repository: ProjectReadRepository,
    ):
        self._user_favorite_read_repository = user_favorite_read_repository
        self._user_favorite_write_repository = user_favorite_write_repository
        self._user_read_repository = user_read_repository
        self._project_read_repository = project_read_repository

    def add_favorite(self, payload: UserFavoriteCreatePayload) -> UserFavorite:
        """
        :raises UserNotFoundException:
        :raises ProjectNotFoundException:
        :raises UserFavoriteNotFoundException:
        """

        self._user_read_repository.get_by_id(payload.user_id)
        self._project_read_repository.get_by_id(payload.project_id)
        search_result: list[UserFavorite] = self._user_favorite_read_repository.get_all(
            UserFavoriteFilter(user_id=payload.user_id, project_id=payload.project_id)
        )
        if search_result:
            logger.warning(
                f"UserFavorite already exists for user_id={payload.user_id.value}, project_id={payload.project_id.value}"
            )
            raise UserFavoriteAlreadyExistsException(
                f"UserFavorite with (user_id={payload.user_id.value}, project_id={payload.project_id.value}) already exists."
            )

        logger.debug("Creating UserFavorite")
        return self._user_favorite_write_repository.create(payload)

    def get_user_favorites(self, user_id: Id) -> list[UserFavorite]:
        """:raises UserNotFoundException:"""

        self._user_read_repository.get_by_id(user_id)
        user_favorites: list[UserFavorite] = self._user_favorite_read_repository.get_all(
            UserFavoriteFilter(user_id=user_id)
        )
        logger.debug(f"Found {len(user_favorites)} favorites with user_id = {user_id.value}")

        return user_favorites

    def delete_by_association_ids(self, user_id: Id, project_id: Id) -> None:
        """:raises UserFavoriteNotFoundException:"""
        self._user_favorite_write_repository.delete_by_association_ids(user_id, project_id)
