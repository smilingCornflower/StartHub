import time
from dataclasses import dataclass
from unittest.mock import Mock

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import SimpleTestCase
from django.utils.datastructures import MultiValueDict
from domain.value_objects.file import Image, ImageFile
from domain.value_objects.news_management.news import NewsContent, NewsSubtitle, NewsTitle, NewsUpdateCommand
from presentation.request_converters.news import request_to_news_update_command
from rest_framework.request import Request
from tests.common.constants import TEST_FILES_PATH


@dataclass
class NewsUpdateTestData:
    title = "Breaking News"
    subtitle = "Important announcement"
    content = "This is the full content of the news article."
    cover_file_name = "cover.jpg"
    image_file_name = "image.jpg"

    title_field = "title"
    subtitle_field = "subtitle"
    content_field = "content"
    cover_field = "cover"
    images_field = "images"

    _image_content = None

    @property
    def img_content(self):
        if self._image_content is None:
            with open(TEST_FILES_PATH / "img.jpg", mode="rb") as f:
                self._image_content = f.read()
        return self._image_content

    def get_cover_file(self):
        return SimpleUploadedFile(name=self.cover_file_name, content=self.img_content, content_type="image/jpeg")

    def get_image_file(self):
        return SimpleUploadedFile(name=self.image_file_name, content=self.img_content, content_type="image/jpeg")

    def get_unnamed_cover_file(self):
        return SimpleUploadedFile(name=None, content=self.img_content, content_type="image/jpeg")


class TestRequestToNewsUpdateCommand(SimpleTestCase):
    def setUp(self):
        self.data = NewsUpdateTestData()

    def apply_function(self, request_data=None, request_files=None):
        request = Mock(spec=Request)
        request.data = request_data or {}
        request.FILES = MultiValueDict(request_files or {})
        return request_to_news_update_command(request)

    def test_empty_data_and_files(self):
        expected = NewsUpdateCommand(
            title=None,
            subtitle=None,
            content=None,
            cover=None,
            images=None,
        )

        result = self.apply_function()
        self.assertEqual(expected, result)

    def test_with_title_only(self):
        data = {self.data.title_field: self.data.title}

        expected = NewsUpdateCommand(
            title=NewsTitle(value=self.data.title),
            subtitle=None,
            content=None,
            cover=None,
            images=None,
        )

        result = self.apply_function(request_data=data)
        self.assertEqual(expected, result)

    def test_with_subtitle_only(self):
        data = {self.data.subtitle_field: self.data.subtitle}

        expected = NewsUpdateCommand(
            title=None,
            subtitle=NewsSubtitle(value=self.data.subtitle),
            content=None,
            cover=None,
            images=None,
        )

        result = self.apply_function(request_data=data)
        self.assertEqual(expected, result)

    def test_with_content_only(self):
        data = {self.data.content_field: self.data.content}

        expected = NewsUpdateCommand(
            title=None,
            subtitle=None,
            content=NewsContent(value=self.data.content),
            cover=None,
            images=None,
        )

        result = self.apply_function(request_data=data)
        self.assertEqual(expected, result)

    def test_with_cover_only(self):
        files = {self.data.cover_field: [self.data.get_cover_file()]}

        expected = NewsUpdateCommand(
            title=None,
            subtitle=None,
            content=None,
            cover=Image(name=self.data.cover_file_name, file=ImageFile(value=self.data.img_content)),
            images=None,
        )

        result = self.apply_function(request_files=files)
        self.assertEqual(expected, result)

    def test_with_cover_without_name(self):
        files = {self.data.cover_field: [self.data.get_unnamed_cover_file()]}

        expected = NewsUpdateCommand(
            title=None,
            subtitle=None,
            content=None,
            cover=Image(name="default_cover_name", file=ImageFile(value=self.data.img_content)),
            images=None,
        )

        result = self.apply_function(request_files=files)
        self.assertEqual(expected, result)

    def test_with_single_image(self):
        files = {self.data.images_field: [self.data.get_image_file()]}

        expected = NewsUpdateCommand(
            title=None,
            subtitle=None,
            content=None,
            cover=None,
            images=[Image(name=self.data.image_file_name, file=ImageFile(value=self.data.img_content))],
        )

        result = self.apply_function(request_files=files)
        self.assertEqual(expected, result)

    def test_with_multiple_images(self):
        files = {self.data.images_field: [self.data.get_image_file(), self.data.get_image_file()]}

        expected = NewsUpdateCommand(
            title=None,
            subtitle=None,
            content=None,
            cover=None,
            images=[
                Image(name=self.data.image_file_name, file=ImageFile(value=self.data.img_content)),
                Image(name=self.data.image_file_name, file=ImageFile(value=self.data.img_content)),
            ],
        )

        result = self.apply_function(request_files=files)
        self.assertEqual(expected, result)

    def test_with_all_fields_and_files(self):
        data = {
            self.data.title_field: self.data.title,
            self.data.subtitle_field: self.data.subtitle,
            self.data.content_field: self.data.content,
        }
        files = {
            self.data.cover_field: [self.data.get_cover_file()],
            self.data.images_field: [self.data.get_image_file(), self.data.get_image_file()],
        }

        expected = NewsUpdateCommand(
            title=NewsTitle(value=self.data.title),
            subtitle=NewsSubtitle(value=self.data.subtitle),
            content=NewsContent(value=self.data.content),
            cover=Image(name=self.data.cover_file_name, file=ImageFile(value=self.data.img_content)),
            images=[
                Image(name=self.data.image_file_name, file=ImageFile(value=self.data.img_content)),
                Image(name=self.data.image_file_name, file=ImageFile(value=self.data.img_content)),
            ],
        )

        result = self.apply_function(request_data=data, request_files=files)
        self.assertEqual(expected, result)
