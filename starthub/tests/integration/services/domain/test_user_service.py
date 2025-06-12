from pathlib import Path
from typing import Any, cast

from config.settings import BASE_DIR
from django.test import TestCase
from domain.constants import PROFILE_PICTURE_PATH
from domain.models.user import User
from domain.services.file import ImageService
from domain.services.user import UserService
from domain.value_objects.common import Id
from domain.value_objects.user import ProfilePictureUploadCommand
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
        cls.user_service = UserService(
            cloud_storage=google_cloud_storage,
            user_read_repository=DjUserReadRepository(),
            user_write_repository=DjUserWriteRepository(),
            image_service=ImageService(),
        )
        cls.image_path = BASE_DIR / "tests/images/frieren.jpg"

    def test_upload_profile_picture(self) -> None:
        with open(self.image_path, mode="rb") as image_file:
            self.user_service.upload_profile_picture(
                payload=ProfilePictureUploadCommand(
                    user_id=Id(value=self.user_valid_data["id"]),
                    file_data=image_file.read(),
                )
            )
        user: User = cast(User, User.objects.filter(id=self.user_valid_data["id"]).first())
        self.assertEqual(user.picture, f"{PROFILE_PICTURE_PATH}/{self.user_valid_data['id']}.jpg")

    def test_generate_url(self) -> None:
        with open(self.image_path, mode="rb") as image_file:
            self.user_service.upload_profile_picture(
                payload=ProfilePictureUploadCommand(
                    user_id=Id(value=self.user_valid_data["id"]),
                    file_data=image_file.read(),
                )
            )
        picture_url: str = self.user_service.get_user_profile_picture(user_id=Id(value=self.user_valid_data["id"]))
        logger.info(f"{picture_url=}")
        self.assertIsNotNone(picture_url)
