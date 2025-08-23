from io import BytesIO

from domain.exceptions.user import ProfilePictureNotFoundException, UserPhoneAlreadyExistException
from domain.models.user import User, UserPhone
from domain.ports.cloud_storage import AbstractCloudStorage
from domain.ports.service import AbstractDomainService
from domain.repositories.user import (
    UserPhoneReadRepository,
    UserPhoneWriteRepository,
    UserReadRepository,
    UserWriteRepository,
)
from domain.services.file import ImageService
from domain.utils.path_provider import PathProvider
from domain.value_objects.cloud_storage import CloudStorageCreateUrlPayload, CloudStorageUploadPayload
from domain.value_objects.common import Description, FirstName, Id, LastName, PhoneNumber
from domain.value_objects.filter import UserPhoneFilter
from domain.value_objects.user_management.user import (
    Email,
    ProfilePictureUploadCommand,
    UserPhoneCreatePayload,
    UserProfile,
    UserUpdateCommand,
    UserUpdatePayload,
)
from loguru import logger


class UserService(AbstractDomainService):
    def __init__(
        self,
        cloud_storage: AbstractCloudStorage,
        user_read_repository: UserReadRepository,
        user_write_repository: UserWriteRepository,
        user_phone_write_repository: UserPhoneWriteRepository,
        user_phone_read_repository: UserPhoneReadRepository,
        image_service: ImageService,
    ):
        self._cloud_storage = cloud_storage
        self._user_read_repository = user_read_repository
        self._user_write_repository = user_write_repository
        self._user_phone_write_repository = user_phone_write_repository
        self._user_phone_read_repository = user_phone_read_repository
        self._image_service = image_service

    def update_user(self, command: UserUpdateCommand) -> None:
        """
        :raises UserNotFoundException:
        :raises NotSupportedImageFormat:
        :raises UserPhoneAlreadyExistException:
        """

        if command.picture_data:
            self.upload_profile_picture(
                ProfilePictureUploadCommand(
                    user_id=command.user_id,
                    file_data=command.picture_data,
                )
            )
        if command.add_phone:
            search_result: list[UserPhone] = self._user_phone_read_repository.get_all(
                UserPhoneFilter(user_id=command.user_id, phone=command.add_phone)
            )
            if search_result:
                logger.exception("UserPhone already exist.")
                raise UserPhoneAlreadyExistException(phone=command.add_phone.value)
            self._user_phone_write_repository.create(
                data=UserPhoneCreatePayload(user_id=command.user_id, phone=command.add_phone)
            )
            logger.debug(f"user_phone {command.add_phone} added.")
        if command.remove_phone:
            self._user_phone_write_repository.delete_by_phone(command.remove_phone)
            logger.debug(f"user_phone {command.remove_phone} removed.")

        self._user_write_repository.update(
            UserUpdatePayload(
                id_=command.user_id,
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

        phones: list[UserPhone] = self._user_phone_read_repository.get_all(UserPhoneFilter(user_id=user_id))
        logger.debug(f"phones = {phones}")
        return UserProfile(
            id_=Id(value=user.id),
            first_name=FirstName(value=user.first_name),
            last_name=LastName(value=user.last_name),
            description=Description(value=user.description),
            email=Email(value=user.email),
            picture=picture_url,
            phone_numbers=[PhoneNumber(value=i.number) for i in phones],
        )
