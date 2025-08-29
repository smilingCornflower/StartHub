from dataclasses import dataclass

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import SimpleTestCase
from domain.exceptions.validation import MissingRequiredFieldException
from domain.value_objects.common import Id
from domain.value_objects.file import ImageFile
from domain.value_objects.project.image import ProjectImageCreateCommand
from presentation.request_converters.project.project_image import request_files_to_project_image_create_command
from tests.common.constants import TEST_FILES_PATH


@dataclass
class ValidProjectImageData:
    project_id = 456
    user_id = 789

    project_image_field = "project_image"


class TestRequestFilesToProjectImageCreateCommand(SimpleTestCase):
    def setUp(self):
        self.valid_dataclass = ValidProjectImageData()

    def test_valid_data(self):
        with open(TEST_FILES_PATH / "img.jpg", mode="rb") as img:
            file_content = img.read()

        uploaded_file = SimpleUploadedFile("test_image.jpg", file_content)
        files = {self.valid_dataclass.project_image_field: uploaded_file}

        expected = ProjectImageCreateCommand(
            user_id=Id(value=self.valid_dataclass.user_id),
            project_id=Id(value=self.valid_dataclass.project_id),
            image_file=ImageFile(value=file_content),
        )

        result = request_files_to_project_image_create_command(
            files, self.valid_dataclass.project_id, self.valid_dataclass.user_id
        )
        self.assertEqual(expected, result)

    def test_missing_project_image_field(self):
        files = {}

        with self.assertRaises(MissingRequiredFieldException):
            request_files_to_project_image_create_command(
                files, self.valid_dataclass.project_id, self.valid_dataclass.user_id
            )
