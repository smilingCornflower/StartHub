from dataclasses import dataclass
from pathlib import Path
from unittest.mock import Mock

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import SimpleTestCase
from domain.exceptions.validation import MissingRequiredFieldException
from domain.value_objects.common import Order
from domain.value_objects.project.media import MediaFile, ProjectMediaCreateCommand, ProjectMediaUpdateCommand
from presentation.request_converters.project.media import (
    request_to_project_media_create_command,
    request_to_project_media_to_update_command,
)
from tests.common.constants import TEST_FILES_PATH


@dataclass
class ValidMediaData:
    new_order = [1, 2, 3]

    project_media_field = "project_media"
    new_order_field = "new_order"


class TestRequestToProjectMediaCreateCommand(SimpleTestCase):
    def setUp(self):
        self.valid_dataclass = ValidMediaData()

    def test_valid_data(self):
        request = Mock()

        with open(TEST_FILES_PATH / "img.jpg", mode="rb") as img:
            file_content = img.read()

        uploaded_file = SimpleUploadedFile("test.jpg", file_content)
        request.FILES = {self.valid_dataclass.project_media_field: uploaded_file}

        expected = ProjectMediaCreateCommand(media=MediaFile(value=file_content))

        result = request_to_project_media_create_command(request)
        self.assertEqual(expected, result)

    def test_missing_project_media_field(self):
        request = Mock()
        request.FILES = {}

        with self.assertRaises(MissingRequiredFieldException):
            request_to_project_media_create_command(request)


class TestRequestToProjectMediaUpdateCommand(SimpleTestCase):
    def setUp(self):
        self.valid_dataclass = ValidMediaData()

    def test_valid_data_with_new_order(self):
        request = Mock()
        request.data = {self.valid_dataclass.new_order_field: self.valid_dataclass.new_order}

        expected = ProjectMediaUpdateCommand(new_order=[Order(value=i) for i in self.valid_dataclass.new_order])
        result = request_to_project_media_to_update_command(request)
        self.assertEqual(expected, result)

    def test_empty_data(self):
        request = Mock()
        request.data = {}

        expected = ProjectMediaUpdateCommand(new_order=None)
        result = request_to_project_media_to_update_command(request)
        self.assertEqual(expected, result)
