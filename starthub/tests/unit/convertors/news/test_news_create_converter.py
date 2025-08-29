from dataclasses import dataclass
from unittest.mock import Mock

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import SimpleTestCase
from django.utils.datastructures import MultiValueDict
from domain.enums.news_tag import NewsTagEnum
from domain.exceptions.news import NewsImageMaxAmountException
from domain.exceptions.validation import MissingRequiredFieldException, ValidationException
from domain.value_objects.common import Id
from domain.value_objects.file import Image, ImageFile
from domain.value_objects.news_management.news import NewsContent, NewsCreateCommand, NewsSubtitle, NewsTitle
from presentation.request_converters.news import request_to_news_create_command
from tests.common.constants import TEST_FILES_PATH


@dataclass
class ValidNewsCreateData:
    user_id = 456
    title = "Test News Title"
    subtitle = "Test News Subtitle"
    content = "Test news content here"
    tags = "politics,economy"
    invalid_tags = "politics,invalid_tag"
    cover_name = "cover.jpg"
    image_names = ["image1.jpg", "image2.jpg"]

    title_field = "title"
    subtitle_field = "subtitle"
    content_field = "content"
    tags_field = "tags"
    cover_field = "cover"
    images_field = "images"

    def to_dict(self):
        return {
            self.title_field: self.title,
            self.subtitle_field: self.subtitle,
            self.content_field: self.content,
            self.tags_field: self.tags,
        }

    def create_files(self, num_images=2, too_many=False):
        with open(TEST_FILES_PATH / "img.jpg", mode="rb") as img_file:
            image_content = img_file.read()

        cover_upload = SimpleUploadedFile(self.cover_name, image_content)

        if too_many:
            num_images = 20  # Exceed limit

        image_uploads = [SimpleUploadedFile(f"image{i}.jpg", image_content) for i in range(num_images)]

        files = MultiValueDict()
        files[self.cover_field] = cover_upload
        files.setlist(self.images_field, image_uploads)
        return files, image_content


class TestRequestToNewsCreateCommand(SimpleTestCase):
    def setUp(self):
        self.valid_dataclass = ValidNewsCreateData()

    def test_valid_data_with_all_fields(self):
        request = Mock()
        request.data = self.valid_dataclass.to_dict()
        request.FILES, image_content = self.valid_dataclass.create_files()

        expected = NewsCreateCommand(
            title=NewsTitle(value=self.valid_dataclass.title),
            subtitle=NewsSubtitle(value=self.valid_dataclass.subtitle),
            content=NewsContent(value=self.valid_dataclass.content),
            author_id=Id(value=self.valid_dataclass.user_id),
            cover=Image(name=self.valid_dataclass.cover_name, file=ImageFile(value=image_content)),
            images=[Image(name=f"image{i}.jpg", file=ImageFile(value=image_content)) for i in range(2)],
            tags=[NewsTagEnum(value=i) for i in self.valid_dataclass.tags.split(",")],
        )

        result = request_to_news_create_command(request, Id(value=self.valid_dataclass.user_id))
        self.assertEqual(result, expected)

    def test_valid_data_without_optional_fields(self):
        request = Mock()
        request.data = {
            self.valid_dataclass.title_field: self.valid_dataclass.title,
            self.valid_dataclass.content_field: self.valid_dataclass.content,
        }
        request.FILES, image_content = self.valid_dataclass.create_files(num_images=0)

        expected = NewsCreateCommand(
            title=NewsTitle(value=self.valid_dataclass.title),
            subtitle=None,
            content=NewsContent(value=self.valid_dataclass.content),
            author_id=Id(value=self.valid_dataclass.user_id),
            cover=Image(name=self.valid_dataclass.cover_name, file=ImageFile(value=image_content)),
            images=[],
            tags=None,
        )

        result = request_to_news_create_command(request, Id(value=self.valid_dataclass.user_id))
        self.assertEqual(result, expected)

    def test_missing_title(self):
        request = Mock()
        data = self.valid_dataclass.to_dict()
        del data[self.valid_dataclass.title_field]
        request.data = data
        request.FILES, _ = self.valid_dataclass.create_files()

        with self.assertRaises(MissingRequiredFieldException):
            request_to_news_create_command(request, Id(value=self.valid_dataclass.user_id))

    def test_missing_cover(self):
        request = Mock()
        request.data = self.valid_dataclass.to_dict()
        request.FILES = MultiValueDict()

        with self.assertRaises(MissingRequiredFieldException):
            request_to_news_create_command(request, Id(value=self.valid_dataclass.user_id))

    def test_invalid_tags(self):
        request = Mock()
        data = self.valid_dataclass.to_dict()
        data[self.valid_dataclass.tags_field] = self.valid_dataclass.invalid_tags
        request.data = data
        request.FILES, _ = self.valid_dataclass.create_files()

        with self.assertRaises(ValidationException):
            request_to_news_create_command(request, Id(value=self.valid_dataclass.user_id))

    def test_too_many_images_raises_exception(self):
        request = Mock()
        request.data = {
            self.valid_dataclass.title_field: self.valid_dataclass.title,
            self.valid_dataclass.content_field: self.valid_dataclass.content,
        }
        request.FILES, _ = self.valid_dataclass.create_files(too_many=True)

        with self.assertRaises(NewsImageMaxAmountException):
            request_to_news_create_command(request, Id(value=self.valid_dataclass.user_id))
