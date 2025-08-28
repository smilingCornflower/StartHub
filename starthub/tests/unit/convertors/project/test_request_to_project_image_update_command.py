from django.test import SimpleTestCase
from domain.exceptions.validation import MissingRequiredFieldException
from domain.value_objects.common import Id, Order
from domain.value_objects.project.image import ProjectImageUpdateCommand
from presentation.request_converters.project.project_images_update_command import (
    request_project_data_to_project_images_update_command,
)


class TestRequestProjectDataToProjectImagesUpdateCommand(SimpleTestCase):
    def test_valid_data_with_new_order(self):
        data = {"new_order": [1, 2, 3]}
        project_id = 123
        user_id = 456

        expected = ProjectImageUpdateCommand(
            project_id=Id(value=123), user_id=Id(value=456), new_order=[Order(value=1), Order(value=2), Order(value=3)]
        )
        result = request_project_data_to_project_images_update_command(data, project_id, user_id)

        self.assertEqual(expected, result)

    def test_empty_new_order(self):
        data = {"new_order": []}
        project_id = 123
        user_id = 456

        expected = ProjectImageUpdateCommand(project_id=Id(value=123), user_id=Id(value=456), new_order=[])
        result = request_project_data_to_project_images_update_command(data, project_id, user_id)
        self.assertEqual(expected, result)

    def test_missing_new_order_field(self):
        data = {}
        project_id = 123
        user_id = 456
        exc = MissingRequiredFieldException
        with self.assertRaises(exc):
            request_project_data_to_project_images_update_command(data, project_id, user_id)
