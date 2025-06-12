import pydantic
from application.dto.user import UserProfileDto
from application.services.gateway import Gateway
from application.services.user import UserAppService
from config.settings import BASE_DIR
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from domain.exceptions.auth import PasswordValidationException
from domain.exceptions.file import NotSupportedImageFormatException
from domain.exceptions.user import UserNotFoundException
from domain.exceptions.validation import EmptyStringException, FirstNameIsTooLongException, LastNameIsTooLongException
from domain.models.user import User
from loguru import logger


class TestUserAppService(TestCase):
    service: UserAppService
    user_id: int

    @classmethod
    def setUpTestData(cls) -> None:
        user = User.objects.create_user(
            email="test.email@example.com",
            first_name="test-name",
            last_name="test-surname",
            password="Pass1234",
        )
        cls.user_id = user.id
        cls.service = Gateway.user_app_service

    def test_success_update_first_name(self) -> None:
        self.service.update_user(
            request_data={"first_name": "AnotherFirstName"},
            request_files=dict(),
            user_id=self.user_id,
        )
        user = User.objects.get(id=self.user_id)
        self.assertEqual(user.first_name, "AnotherFirstName")

    def test_success_update_last_name(self) -> None:
        self.service.update_user(
            request_data={"last_name": "AnotherLastName"},
            request_files=dict(),
            user_id=self.user_id,
        )
        user = User.objects.get(id=self.user_id)
        self.assertEqual(user.last_name, "AnotherLastName")

    def test_success_update_password(self) -> None:
        self.service.update_user(
            request_data={"password": "AnotherPass1234"},
            request_files=dict(),
            user_id=self.user_id,
        )
        user = User.objects.get(id=self.user_id)
        self.assertTrue(user.check_password("AnotherPass1234"))

    def test_name_is_too_long(self) -> None:
        with self.assertRaises(FirstNameIsTooLongException):
            self.service.update_user(
                request_data={"first_name": "a" * 51},
                request_files=dict(),
                user_id=self.user_id,
            )
        with self.assertRaises(LastNameIsTooLongException):
            self.service.update_user(
                request_data={"last_name": "a" * 51},
                request_files=dict(),
                user_id=self.user_id,
            )

    def test_empty_strings(self) -> None:
        for field in ["first_name", "last_name", "password"]:
            with self.subTest(field=field):
                with self.assertRaises(EmptyStringException):
                    self.service.update_user(
                        request_data={field: ""},
                        request_files=dict(),
                        user_id=self.user_id,
                    )

    def test_another_data_types(self) -> None:
        for field in ["first_name", "last_name", "password"]:
            with self.subTest(field=field):
                with self.assertRaises(pydantic.ValidationError):
                    self.service.update_user(
                        request_data={field: 1234},
                        request_files=dict(),
                        user_id=self.user_id,
                    )

    def test_fails_password_validation(self) -> None:
        with self.assertRaises(PasswordValidationException):
            self.service.update_user(
                request_data={"password": "weak-pass"},
                request_files=dict(),
                user_id=self.user_id,
            )

    def test_user_not_found(self) -> None:
        with self.assertRaises(UserNotFoundException):
            self.service.update_user(
                request_data={"first_name": "AnotherFirstName"},
                request_files=dict(),
                user_id=-1,
            )

    def test_success_image_upload(self) -> None:
        img_path = BASE_DIR / "tests/images/frieren.jpg"
        with open(img_path, "rb") as f:
            data = f.read()
        img_file = SimpleUploadedFile(name="frieren.jpg", content=data, content_type="image/jpeg")
        self.service.update_user(
            request_data=dict(),
            request_files={"profile_picture": img_file},
            user_id=self.user_id,
        )
        user = User.objects.get(id=self.user_id)
        logger.debug(f"{user.picture=}")
        self.assertTrue(user.picture)

    def test_not_supported_image_format_upload(self) -> None:
        img_path = BASE_DIR / "tests/images/galaxy.tif"
        with open(img_path, "rb") as f:
            data = f.read()
        img_file = SimpleUploadedFile(name="galaxy.tif", content=data, content_type="image/tiff")
        with self.assertRaises(NotSupportedImageFormatException):
            self.service.update_user(
                request_data=dict(), request_files={"profile_picture": img_file}, user_id=self.user_id
            )

    def test_success_get_user_profile(self) -> None:
        profile: UserProfileDto = self.service.get_user_profile(self.user_id)

        logger.debug(f"{profile=}")
        self.assertEqual(profile.first_name, "test-name")
        self.assertEqual(profile.last_name, "test-surname")
        self.assertEqual(profile.email, "test.email@example.com")
        self.assertEqual(profile.picture, None)

    def test_success_get_user_own_profile(self) -> None:
        profile: UserProfileDto = self.service.get_user_own_profile(self.user_id)

        logger.debug(f"{profile=}")
        self.assertEqual(profile.first_name, "test-name")
        self.assertEqual(profile.last_name, "test-surname")
        self.assertEqual(profile.email, "test.email@example.com")
        self.assertEqual(profile.picture, None)
