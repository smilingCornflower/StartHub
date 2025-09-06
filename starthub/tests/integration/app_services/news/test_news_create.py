from pathlib import Path

from application.builders.app_service.news import NewsAppServiceBuilder
from django.test import TestCase
from domain.constants import NEWS_IMAGES_MAX_AMOUNT
from domain.enums.news_tag import NewsTagEnum
from domain.enums.permission import ActionEnum, ScopeEnum
from domain.exceptions.news import NewsImageContentAndFileMismatchException, NewsImageMaxAmountException
from domain.exceptions.permissions import AddDeniedPermissionException
from domain.models.news_management.news import News
from domain.value_objects.cloud_storage import CloudStorageDeletePayload
from domain.value_objects.common import Id
from domain.value_objects.file import Image, ImageFile
from domain.value_objects.news_management.news import NewsContent, NewsCreateCommand, NewsSubtitle, NewsTitle
from infrastructure.cloud_storages.google import GoogleCloudStorage, GoogleCloudStorageFactory
from tests.common.builders import create_user_with_permission, get_random_user, get_test_user
from tests.common.constants import TEST_FILES_PATH


class TestNewsCreateAppService(TestCase):
    def setUp(self):
        self.service = NewsAppServiceBuilder.create_service()

        self.user, _, _ = create_user_with_permission(
            model=News,
            action=ActionEnum.ADD,
            scope=ScopeEnum.ANY,
        )
        self.random_user = get_random_user()

        self.user_id = Id(value=self.user.id)
        self.random_user_id = Id(value=self.random_user.id)

        self._image_content = None

        self.storage = GoogleCloudStorageFactory.create()

    @property
    def image_content(self):
        if self._image_content is None:
            with open(TEST_FILES_PATH / "img.jpg", mode="rb") as f:
                self._image_content = f.read()
        return self._image_content

    def get_command(self):
        command = NewsCreateCommand(
            title=NewsTitle(value="News"),
            subtitle=NewsSubtitle(value="Subtitle"),
            content=NewsContent(value="Content and image: ![image](art.jpg)"),
            author_id=self.user_id,
            cover=Image(name="cover.jpg", file=ImageFile(value=self.image_content)),
            images=[Image(name="art.jpg", file=ImageFile(value=self.image_content))],
            tags=[NewsTagEnum.WORLD, NewsTagEnum.SPORTS],
        )
        return command

    def test_create_with_valid_data(self):
        command = self.get_command()
        news_id = self.service.create(user_id=self.user_id, news_create_command=command)
        news = News.objects.get(id=news_id)

        self.assertEqual(news.title, command.title.value)
        self.assertEqual(news.subtitle, command.subtitle.value)
        self.assertEqual(news.author_id, self.user_id.value)

        covert_path = news.cover
        image_path = news.images.all().first().image

        self.assertTrue(self.storage.check_url_exists(url=covert_path))
        self.assertTrue(self.storage.check_url_exists(url=image_path))

        img_name = Path(image_path).name
        self.assertIn(img_name, news.content)

        self.storage.delete_file(payload=CloudStorageDeletePayload(file_path=covert_path))
        self.storage.delete_file(payload=CloudStorageDeletePayload(file_path=image_path))

    def test_create_with_user_without_permissions(self):
        command = self.get_command()
        with self.assertRaises(AddDeniedPermissionException):
            self.service.create(user_id=self.random_user_id, news_create_command=command)

    def test_create_with_more_than_max_allowed_images_amount(self):
        command = self.get_command()
        images = [
            Image(name=f"img_{i}.jpg", file=ImageFile(value=self.image_content))
            for i in range(NEWS_IMAGES_MAX_AMOUNT + 1)
        ]
        content = "Conteant & Images: " + ", ".join([f"![]({i.name})" for i in images])
        command.content = NewsContent(value=content)
        command.images = images

        with self.assertRaises(NewsImageMaxAmountException):
            self.service.create(user_id=self.user_id, news_create_command=command)

    def test_create_with_unused_files_in_content(self):
        command = self.get_command()
        command.content = NewsContent(value="No images content")

        with self.assertRaises(NewsImageContentAndFileMismatchException):
            self.service.create(user_id=self.user_id, news_create_command=command)

    def test_create_file_used_in_content_doesnt_exist_in_files_or_in_database(self):
        command = self.get_command()
        command.content = NewsContent(value="content, ![non-existing-image](image.jpeg)")
        command.images = []
        with self.assertRaises(NewsImageContentAndFileMismatchException):
            self.service.create(user_id=self.user_id, news_create_command=command)
