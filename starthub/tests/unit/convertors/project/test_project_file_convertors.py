from dataclasses import dataclass
from unittest.mock import Mock

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import SimpleTestCase
from domain.exceptions.validation import MissingRequiredFieldException
from domain.value_objects.file import FileVo
from domain.value_objects.project.project_file import ProjectFileCreateCommand, ProjectFileName
from presentation.request_converters.project.project_file import request_to_project_file_create_command
from tests.common.constants import TEST_FILES_PATH


@dataclass
class ValidProjectFileData:
    file_name = "test_file.pdf"

    project_file_field = "project_file"


class TestRequestToProjectFileCreateCommand(SimpleTestCase):
    def setUp(self):
        self.valid_dataclass = ValidProjectFileData()

    def test_valid_data_with_name(self):
        request = Mock()

        with open(TEST_FILES_PATH / "file.pdf", mode="rb") as file:
            file_content = file.read()

        uploaded_file = SimpleUploadedFile(self.valid_dataclass.file_name, file_content)
        request.FILES = {self.valid_dataclass.project_file_field: uploaded_file}

        expected = ProjectFileCreateCommand(
            file=FileVo(value=file_content), name=ProjectFileName(value=self.valid_dataclass.file_name)
        )
        result = request_to_project_file_create_command(request)
        self.assertEqual(expected, result)

    def test_valid_data_without_name(self):
        request = Mock()

        with open(TEST_FILES_PATH / "file.pdf", mode="rb") as file:
            file_content = file.read()

        uploaded_file = SimpleUploadedFile(None, file_content)
        request.FILES = {self.valid_dataclass.project_file_field: uploaded_file}

        expected = ProjectFileCreateCommand(file=FileVo(value=file_content), name=None)

        result = request_to_project_file_create_command(request)
        self.assertEqual(expected, result)

    def test_missing_project_file_field(self):
        request = Mock()
        request.FILES = {}

        with self.assertRaises(MissingRequiredFieldException):
            request_to_project_file_create_command(request)
