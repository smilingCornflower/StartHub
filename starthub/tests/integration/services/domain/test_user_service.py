from pathlib import Path
from typing import Any, Callable, cast

from application.service_factories.domain_service.user import UserServiceFactory
from config.settings import BASE_DIR
from django.test import TestCase
from domain.constants import StorageLocations
from domain.exceptions.user import UserNotFoundException, UserPhoneAlreadyExistException
from domain.models.user import User
from domain.services.file import ImageService
from domain.services.user_management import UserService
from domain.value_objects.common import Description, FirstName, Id, LastName, PhoneNumber
from domain.value_objects.user import ProfilePictureUploadCommand, RawPassword, UserProfile, UserUpdateCommand
from infrastructure.cloud_storages.google import google_cloud_storage
from infrastructure.repositories.user import DjUserReadRepository, DjUserWriteRepository
from loguru import logger


class TestUserService(TestCase):
    user: User
    user_service: UserService
    image_path: Path
    user_valid_data: dict[str, Any]

    @classmethod
    def setUpTestData(cls) -> None:
        user = User.objects.create_user(
            email="test.mail@example.com",
            first_name="name",
            last_name="surname",
            password="Pass1234",
        )

        cls.user_valid_data = {
            "id": user.id,
            "email": "test.mail@example.com",
            "first_name": "name",
            "last_name": "surname",
        }
        cls.user_service = UserServiceFactory.create_service()
        cls.image_path = BASE_DIR / "tests/images/frieren.jpg"

    def check_raises(self, exc: type[Exception], func: Callable[[Any], Any]) -> None:
        self.assertTrue(f":raises {exc.__name__}:" in func.__doc__)

    def test_update_first_name(self) -> None:
        self.user_service.update_user(
            command=UserUpdateCommand(
                user_id=Id(value=self.user_valid_data["id"]), first_name=FirstName(value="another_name")
            )
        )
        user: User = cast(User, User.objects.filter(id=self.user_valid_data["id"]).first())
        self.assertEqual(user.first_name, "another_name")

    def test_update_last_name(self) -> None:
        self.user_service.update_user(
            command=UserUpdateCommand(
                user_id=Id(value=self.user_valid_data["id"]), last_name=LastName(value="another_surname")
            )
        )
        user: User = cast(User, User.objects.filter(id=self.user_valid_data["id"]).first())
        self.assertEqual(user.last_name, "another_surname")

    def test_update_description(self):
        self.user_service.update_user(
            command=UserUpdateCommand(
                user_id=Id(value=self.user_valid_data["id"]), description=Description(value="another_description")
            )
        )
        user: User = cast(User, User.objects.filter(id=self.user_valid_data["id"]).first())
        self.assertEqual(user.description, "another_description")

    def test_update_password(self):
        self.user_service.update_user(
            command=UserUpdateCommand(
                user_id=Id(value=self.user_valid_data["id"]), password=RawPassword(value="GoodPass1234")
            )
        )
        user: User = cast(User, User.objects.filter(id=self.user_valid_data["id"]).first())
        self.assertTrue(user.check_password("GoodPass1234"))

    def test_add_phone(self):
        self.user_service.update_user(
            command=UserUpdateCommand(
                user_id=Id(value=self.user_valid_data["id"]), add_phone=PhoneNumber(value="+77774567890")
            )
        )
        user: User = cast(User, User.objects.filter(id=self.user_valid_data["id"]).first())
        self.assertTrue(user.phones.all().first(), "+71234567890")

    def test_remove_phone(self):
        self.user_service.update_user(
            command=UserUpdateCommand(
                user_id=Id(value=self.user_valid_data["id"]), add_phone=PhoneNumber(value="+77774567890")
            )
        )
        self.user_service.update_user(
            command=UserUpdateCommand(
                user_id=Id(value=self.user_valid_data["id"]), remove_phone=PhoneNumber(value="+77774567890")
            )
        )
        user: User = cast(User, User.objects.filter(id=self.user_valid_data["id"]).first())
        self.assertIsNone(user.phones.all().first())

    def test_remove_not_existing_phone(self):
        """delete phone method is idempotent"""
        self.user_service.update_user(
            command=UserUpdateCommand(
                user_id=Id(value=self.user_valid_data["id"]), remove_phone=PhoneNumber(value="+77774567890")
            )
        )

    def test_phone_already_exists(self):
        self.user_service.update_user(
            command=UserUpdateCommand(
                user_id=Id(value=self.user_valid_data["id"]), add_phone=PhoneNumber(value="+77774567890")
            )
        )
        with self.assertRaises(UserPhoneAlreadyExistException):
            self.user_service.update_user(
                command=UserUpdateCommand(
                    user_id=Id(value=self.user_valid_data["id"]), add_phone=PhoneNumber(value="+77774567890")
                )
            )
        self.check_raises(UserPhoneAlreadyExistException, self.user_service.update_user)

    def test_upload_profile_picture(self) -> None:
        with open(self.image_path, mode="rb") as image_file:
            self.user_service.upload_profile_picture(
                command=ProfilePictureUploadCommand(
                    user_id=Id(value=self.user_valid_data["id"]),
                    file_data=image_file.read(),
                )
            )
        user: User = cast(User, User.objects.filter(id=self.user_valid_data["id"]).first())
        self.assertEqual(user.picture, f"{StorageLocations.PROFILE_PICTURE_PATH}/{self.user_valid_data['id']}.jpg")

    def test_generate_profile_picture_url(self) -> None:
        with open(self.image_path, mode="rb") as image_file:
            self.user_service.upload_profile_picture(
                command=ProfilePictureUploadCommand(
                    user_id=Id(value=self.user_valid_data["id"]),
                    file_data=image_file.read(),
                )
            )
        picture_url: str = self.user_service.get_user_profile_picture(user_id=Id(value=self.user_valid_data["id"]))
        logger.info(f"{picture_url=}")
        self.assertIsNotNone(picture_url)

    def test_get_user_profile(self):
        profile: UserProfile = self.user_service.get_user_profile(Id(value=self.user_valid_data["id"]))

        self.assertEqual(profile.email.value, "test.mail@example.com")
        self.assertEqual(profile.first_name.value, "name")
        self.assertEqual(profile.last_name.value, "surname")
        self.assertEqual(profile.description.value, "")
        self.assertEqual(profile.picture, None)
        self.assertEqual(profile.phone_numbers, list())

    def test_get_user_profile_of_not_existing_user(self):
        with self.assertRaises(UserNotFoundException):
            self.user_service.get_user_profile(Id(value=-1))
