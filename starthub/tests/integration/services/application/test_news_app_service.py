import re
from copy import deepcopy
from pathlib import Path
from pprint import pformat
from typing import Any, Callable

import pydantic
from application.dto.news import NewsShortDto
from application.service_factories.app_service.news import NewsAppServiceFactory, NewsServiceBuilder
from application.services.news import NewsAppService
from config.settings import BASE_DIR
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import QueryDict
from django.test import TestCase
from django.utils.datastructures import MultiValueDict
from domain.exceptions.file import NotSupportedImageFormatException
from domain.exceptions.news import NewsImageContentAndFileMismatchException
from domain.exceptions.permissions import (
    AddDeniedPermissionException,
    DeleteDeniedPermissionException,
    UpdateDeniedPermissionException,
)
from domain.exceptions.validation import MissingFileExcpetion, MissingRequiredFieldException
from domain.models.news import News, NewsImage
from domain.models.role import Role
from domain.models.user import User
from domain.value_objects.cloud_storage import CloudStorageCreateUrlPayload
from domain.value_objects.news import NewsContent
from infrastructure.cloud_storages.google import google_cloud_storage
from loguru import logger


class TestCreateNewsAppService(TestCase):
    user_id: int
    blogger_id: int

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(email="test@example.com", password="ValidPass1234")
        blogger = User.objects.create_user(email="blogger@example.com", password="ValidPass1234")

        role = Role.objects.get(name="blogger")
        blogger.roles.add(role)

        cls.user_id = user.id
        cls.blogger_id = blogger.id

    def setUp(self):
        self.service = NewsAppServiceFactory.create_service()
        self.cloud_service = google_cloud_storage

        image = BASE_DIR / "tests/images/miku.jpg"

        with open(image, mode="rb") as file:
            image_data = file.read()
        upload_image = SimpleUploadedFile(name=image.name, content=image_data, content_type="image/jpeg")

        self.valid_data = QueryDict(mutable=True)
        self.valid_data.update({"title": "News Title", "content": f"Simple content\n" f"![image]({image.name})"})
        self.files = MultiValueDict(
            {
                "images": [upload_image],
                "cover": [upload_image],
            }
        )

    def check_raises(self, exc: type[Exception], func: Callable[..., Any]) -> None:
        self.assertTrue(f":raises {exc.__name__}:" in func.__doc__)

    def test_create_success(self):
        news_id: int = self.service.create(
            request_data=self.valid_data, request_files=self.files, user_id=self.blogger_id
        )
        news = News.objects.get(id=news_id)
        image: NewsImage = list(news.images.all())[0]

        cover_url: str = self.cloud_service.create_url(payload=CloudStorageCreateUrlPayload(file_path=news.cover))
        image_url: str = self.cloud_service.create_url(payload=CloudStorageCreateUrlPayload(file_path=image.image))

        self.assertIsInstance(cover_url, str)
        self.assertIsInstance(image_url, str)
        self.assertTrue(cover_url)
        self.assertTrue(image_url)

        content = f"Simple content\n![image]({Path(image.image).name})"
        self.assertEqual(news.title, self.valid_data["title"])
        self.assertEqual(news.content, content)

    def test_create_by_not_blogger(self):
        with self.assertRaises(AddDeniedPermissionException):
            self.service.create(request_data=self.valid_data, request_files=self.files, user_id=self.user_id)

    def test_create_missing_fields(self):
        logger.warning("test_create_missing_fields()")

        self.check_raises(MissingRequiredFieldException, self.service.create)
        with self.subTest("Missing title field test"):
            with self.assertRaises(MissingRequiredFieldException):
                valid_data_copy = deepcopy(self.valid_data)
                valid_data_copy.pop("title")
                self.service.create(request_data=valid_data_copy, request_files=self.files, user_id=self.blogger_id)

        with self.subTest("Missing content field test"):
            with self.assertRaises(MissingRequiredFieldException):
                valid_data_copy = deepcopy(self.valid_data)
                valid_data_copy.pop("content")
                self.service.create(request_data=valid_data_copy, request_files=self.files, user_id=self.blogger_id)

        with self.subTest("Missing cover field test"):
            with self.assertRaises(MissingRequiredFieldException):
                requrest_files_copy = deepcopy(self.files)
                requrest_files_copy.pop("cover")
                self.service.create(
                    request_data=self.valid_data, request_files=requrest_files_copy, user_id=self.blogger_id
                )

    def test_missing_image_which_provided_in_content(self):
        """If image name provided in content, the corresponding file must be present in files"""
        with self.assertRaises(MissingFileExcpetion):
            requrest_files_copy = deepcopy(self.files)
            requrest_files_copy.pop("images")
            self.service.create(
                request_data=self.valid_data, request_files=requrest_files_copy, user_id=self.blogger_id
            )
        self.check_raises(MissingFileExcpetion, self.service.create)

    def test_create_with_invalid_cover(self):
        docs_file = BASE_DIR / "tests/files/articles.docx"

        with open(docs_file, mode="rb") as file:
            docs_data = file.read()

        upload_image = SimpleUploadedFile(name="miku.jpg", content=docs_data, content_type="image/jpeg")
        files_copy = deepcopy(self.files)
        files_copy.setlist("images", [upload_image])
        logger.debug(f"files_copy: {files_copy}")

        with self.assertRaises(NotSupportedImageFormatException):
            self.service.create(request_data=self.valid_data, request_files=files_copy, user_id=self.blogger_id)
        self.check_raises(NotSupportedImageFormatException, self.service.create)

    def test_create_with_invalid_types(self):
        self.check_raises(pydantic.ValidationError, self.service.create)
        with self.subTest("Invalid type for title"):
            with self.assertRaises(pydantic.ValidationError):
                valid_data_copy = deepcopy(self.valid_data)
                valid_data_copy["title"] = 12345
                self.service.create(request_data=valid_data_copy, request_files=self.files, user_id=self.blogger_id)

        with self.subTest("Invalid type for content"):
            with self.assertRaises(pydantic.ValidationError):
                valid_data_copy = deepcopy(self.valid_data)
                valid_data_copy["content"] = 12345
                self.service.create(request_data=valid_data_copy, request_files=self.files, user_id=self.blogger_id)

    def test_create_without_images(self):
        valid_data_copy = deepcopy(self.valid_data)
        valid_data_copy["content"] = f"Content without images"

        news_id: int = self.service.create(
            request_data=self.valid_data, request_files=self.files, user_id=self.blogger_id
        )
        self.assertIsInstance(news_id, int)


class TestUploadNewsAppService(TestCase):
    service: NewsAppService

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(email="test@example.com", password="ValidPass1234")
        blogger = User.objects.create_user(email="blogger@example.com", password="ValidPass1234")

        role = Role.objects.get(name="blogger")
        blogger.roles.add(role)

        cls.user_id = user.id
        cls.blogger_id = blogger.id

        cls.cloud_service = google_cloud_storage

        image = BASE_DIR / "tests/images/miku.jpg"

        with open(image, mode="rb") as file:
            image_data = file.read()
        upload_image = SimpleUploadedFile(name=image.name, content=image_data, content_type="image/jpeg")

        valid_data = QueryDict(mutable=True)
        valid_data.update({"title": "News Title", "content": f"Simple content\n" f"![image]({image.name})"})
        files = MultiValueDict(
            {
                "images": [upload_image],
                "cover": [upload_image],
            }
        )
        service = NewsAppServiceFactory.create_service()
        cls.news_id = service.create(request_data=valid_data, request_files=files, user_id=cls.blogger_id)

    def check_raises(self, exc: type[Exception], func: Callable[[Any], Any]) -> None:
        self.assertTrue(f":raises {exc.__name__}:" in func.__doc__)

    def setUp(self):
        self.service = NewsAppServiceFactory.create_service()

    def test_update_title(self):
        anther_title = "Another Title"
        self.service.update(
            request_data={"title": anther_title},
            request_files=MultiValueDict(),
            user_id=self.blogger_id,
            news_id=self.news_id,
        )
        self.assertEqual(News.objects.get(id=self.news_id).title, anther_title)

    def test_update_cover(self):
        old_cover_path = News.objects.get(id=self.news_id).cover

        image_path = BASE_DIR / "tests/images/Kawaii.png"
        with open(image_path, mode="rb") as image_file:
            image = SimpleUploadedFile(name=image_file.name, content=image_file.read())

        self.service.update(
            request_data=dict(),
            request_files=MultiValueDict({"cover": [image]}),
            user_id=self.blogger_id,
            news_id=self.news_id,
        )

        new_cover_path = News.objects.get(id=self.news_id).cover
        self.assertNotEqual(new_cover_path, old_cover_path)

    def test_update_content_without_changing_images(self):
        old_content = News.objects.get(id=self.news_id).content
        new_content = old_content + "\nNew line of the news."

        logger.debug(f"{old_content=}")
        logger.debug(f"{new_content=}")

        self.service.update(
            request_data={"content": new_content},
            request_files=MultiValueDict(),
            user_id=self.blogger_id,
            news_id=self.news_id,
        )

        content = News.objects.get(id=self.news_id).content
        news_images = list(NewsImage.objects.filter(news_id=self.news_id))
        logger.debug(f"{news_images=}")
        logger.debug(f"content after updating = {repr(content)}")

        self.assertEqual(content, new_content)

    def test_update_content_image(self):
        logger.warning("test_update_content_image()")
        old_content = News.objects.get(id=self.news_id).content
        new_content = old_content + "\nNew image: ![another image](Kawaii.png)."

        image_path = BASE_DIR / "tests/images/Kawaii.png"
        with open(image_path, mode="rb") as image_file:
            image = SimpleUploadedFile(name=image_file.name, content=image_file.read())

        self.service.update(
            request_data={"content": new_content},
            request_files=MultiValueDict({"images": [image]}),
            user_id=self.blogger_id,
            news_id=self.news_id,
        )

        news_images = list(NewsImage.objects.filter(news_id=self.news_id))
        news_content = News.objects.get(id=self.news_id).content
        logger.info(f"news_images:\n {pformat(news_images)}")
        logger.info(f"news_content:\n {pformat(news_content)}")
        news_service = NewsServiceBuilder.create_service()

        all_images = news_service.get_all_image_names_from_content(content=NewsContent(value=news_content))
        logger.info(f"all_images: \n {pformat(all_images)}")

        self.assertEqual(len(all_images), 2)
        for image in NewsImage.objects.filter(id=self.news_id).all():
            image_name = Path(image.image).name
            logger.debug(f"checking image: {image_name}")
            self.assertTrue(image_name in all_images)

    def test_update_denied(self):
        self.check_raises(UpdateDeniedPermissionException, func=self.service.update)
        with self.assertRaises(UpdateDeniedPermissionException):
            self.service.update(
                request_data={"title": "Another Title"},
                request_files=MultiValueDict(),
                user_id=self.user_id,
                news_id=self.news_id,
            )

    def test_update_title_with_invalid_type(self):
        self.check_raises(pydantic.ValidationError, self.service.update)
        with self.assertRaises(pydantic.ValidationError):
            self.service.update(
                request_data={"title": 12345},
                request_files=MultiValueDict(),
                user_id=self.blogger_id,
                news_id=self.news_id,
            )

    def test_images_files_not_used_in_content(self):
        old_content = News.objects.get(id=self.news_id).content
        new_content = old_content + "\nNew line of the news."

        extra_image_path = BASE_DIR / "tests/images/frieren.jpg"
        with open(extra_image_path, mode="rb") as f:
            extra_image = SimpleUploadedFile(name=f.name, content=f.read())

        with self.assertRaises(NewsImageContentAndFileMismatchException):
            self.service.update(
                request_data={"content": new_content},
                request_files=MultiValueDict({"images": [extra_image]}),
                user_id=self.blogger_id,
                news_id=self.news_id,
            )
        self.check_raises(NewsImageContentAndFileMismatchException, self.service.update)

    def test_image_name_in_content_not_exists_in_files(self):
        old_content = News.objects.get(id=self.news_id).content
        new_content = old_content + "\nExtra image: ![some image](not_existing_image.jpeg)"

        with self.assertRaises(NewsImageContentAndFileMismatchException):
            self.service.update(
                request_data={"content": new_content},
                request_files=MultiValueDict(),
                user_id=self.blogger_id,
                news_id=self.news_id,
            )
        self.check_raises(NewsImageContentAndFileMismatchException, self.service.update)


class TestGetNewsAppService(TestCase):
    def setUp(self):
        self.service = NewsAppServiceFactory.create_service()

    @classmethod
    def setUpTestData(cls):
        cls.content_pattern = re.compile(
            r"^Content \d\n"
            r"image1: !\[image1\]\([a-f0-9\-]{36}\.jpg\)\n"
            r"image2: !\[image2\]\([a-f0-9\-]{36}\.jpg\)$"
        )

        user = User.objects.create_user(email="test@example.com", password="ValidPass1234")
        blogger = User.objects.create_user(email="blogger@example.com", password="ValidPass1234")

        role = Role.objects.get(name="blogger")
        blogger.roles.add(role)

        cls.user_id = user.id
        cls.blogger_id = blogger.id

        cls.amount = 5

        service = NewsAppServiceFactory.create_service()
        img1_path = BASE_DIR / "tests/images/frieren.jpg"
        img2_path = BASE_DIR / "tests/images/miku.jpg"

        first_news_id = None

        for i in range(1, cls.amount + 1):
            with open(img1_path, mode="rb") as f:
                image1 = SimpleUploadedFile(name=f.name, content=f.read())

            with open(img2_path, mode="rb") as f:
                image2 = SimpleUploadedFile(name=f.name, content=f.read())
            news_id = service.create(
                request_data={
                    "title": f"News Title {i}",
                    "content": f"Content {i}\nimage1: ![image1](frieren.jpg)\nimage2: ![image2](miku.jpg)",
                },
                request_files=MultiValueDict(
                    {
                        "images": [image1, image2],
                        "cover": [image1],
                    }
                ),
                user_id=cls.blogger_id,
            )
            if i == 1:
                first_news_id = news_id
        cls.first_news_id = first_news_id

    def test_get_many(self):
        all_news: list[NewsShortDto] = self.service.get(query_params=QueryDict("limit=10"))
        logger.debug(f"news: \n{pformat(all_news)}")

        self.assertEqual(len(all_news), self.amount)

        for i, news in enumerate(reversed(all_news), 1):
            with self.subTest(f"news number: {i}"):
                self.assertEqual(news.title, f"News Title {i}")
                self.assertEqual(news.author_id, self.blogger_id)
                self.assertTrue(news.cover.startswith("https://storage.googleapis.com/starthub-bucket/test/news"))

    def test_get_many_with_limit(self):
        limit_number = 3
        all_news: list[NewsShortDto] = self.service.get(query_params=QueryDict(f"limit={limit_number}"))
        self.assertEqual(len(all_news), limit_number)

    def test_get_many_with_last_id(self):
        all_news: list[NewsShortDto] = self.service.get(
            query_params=QueryDict(f"limit=10&last_id={self.first_news_id + 2}")
        )
        logger.debug(f"all_news: \n{pformat(all_news)}")
        all_news_ids = [i.id for i in all_news]
        self.assertEqual(all_news_ids, [self.first_news_id + 1, self.first_news_id])

    def test_get_one(self):
        news_full_dto = self.service.get(query_params=QueryDict(f"limit=10"), news_id=self.first_news_id)
        logger.debug(f"news_full_dto: \n {pformat(news_full_dto)}")
        self.assertTrue(self.content_pattern.fullmatch(news_full_dto.content))
        self.assertEqual(len(news_full_dto.images), 2)

        for i in news_full_dto.images:
            self.assertIn(i.image_name, news_full_dto.content)
            self.assertTrue(i.image_url.startswith("https://storage.googleapis.com/starthub-bucket/test/news"))


class TestDeleteNewsAppService(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(email="test@example.com", password="ValidPass1234")
        blogger = User.objects.create_user(email="blogger@example.com", password="ValidPass1234")

        role = Role.objects.get(name="blogger")
        blogger.roles.add(role)

        cls.user_id = user.id
        cls.blogger_id = blogger.id

        img_path = BASE_DIR / "tests/images/frieren.jpg"
        with open(img_path, mode="rb") as f:
            image1 = SimpleUploadedFile(name=f.name, content=f.read())

        service = NewsAppServiceFactory.create_service()
        news_id = service.create(
            request_data={"title": f"News Title", "content": f"Content\nimage1: ![image1](frieren.jpg)"},
            request_files=MultiValueDict(
                {
                    "images": [image1],
                    "cover": [image1],
                }
            ),
            user_id=cls.blogger_id,
        )
        cls.news_id = news_id

    def setUp(self):
        self.service = NewsAppServiceFactory.create_service()
        self.cloud_storage = google_cloud_storage

    def check_raises(self, exc: type[Exception], func: Callable[[Any], Any]) -> None:
        self.assertTrue(f":raises {exc.__name__}:" in func.__doc__)

    def test_delete_denied(self):
        with self.assertRaises(DeleteDeniedPermissionException):
            self.service.delete(news_id=self.news_id, user_id=self.user_id)
        self.check_raises(DeleteDeniedPermissionException, self.service.delete)

    def test_delete_successfull(self):
        news = News.objects.filter(id=self.news_id).first()
        cover_url = news.cover
        image_urls = [i.image for i in news.images.all()]

        logger.debug({f"{cover_url=}"})
        logger.debug({f"{image_urls=}"})

        check_cover_before = self.cloud_storage.check_url_exists(url=cover_url)
        logger.debug(f"{check_cover_before=}")
        self.assertTrue(check_cover_before)
        for img_url in image_urls:
            self.assertTrue(self.cloud_storage.check_url_exists(url=img_url))

        self.service.delete(news_id=self.news_id, user_id=self.blogger_id)
        self.assertFalse(News.objects.filter(id=self.news_id).exists())

        check_cover_after = self.cloud_storage.check_url_exists(url=cover_url)
        logger.debug(f"{check_cover_after=}")

        self.assertFalse(check_cover_after)
        for img_url in image_urls:
            self.assertFalse(self.cloud_storage.check_url_exists(url=img_url))
