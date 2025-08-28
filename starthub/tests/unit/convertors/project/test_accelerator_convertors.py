from django.test import SimpleTestCase
from unittest.mock import Mock

from domain.exceptions.validation import MissingRequiredFieldException
from domain.value_objects.common import Description
from domain.value_objects.project.accelerator import (
    AcceleratorName,
    ProjectAcceleratorCreateCommand,
    ProjectAcceleratorUpdateCommand,
)
from presentation.request_converters.project.accelerator import (
    request_to_project_accelerator_create_command,
    request_to_project_accelerator_update_command,
)


class TestRequestToProjectAcceleratorCreateCommand(SimpleTestCase):
    def test_valid_data(self):
        request = Mock()
        request.data = {
            "name": "Test Accelerator",
            "description": "Test Description"
        }

        expected = ProjectAcceleratorCreateCommand(
            name=AcceleratorName(value="Test Accelerator"),
            description=Description(value="Test Description")
        )

        result = request_to_project_accelerator_create_command(request)
        self.assertEqual(expected, result)

    def test_missing_name_field(self):
        request = Mock()
        request.data = {"description": "Test Description"}

        with self.assertRaises(MissingRequiredFieldException):
            request_to_project_accelerator_create_command(request)

    def test_missing_description_field(self):
        request = Mock()
        request.data = {"name": "Test Accelerator"}

        with self.assertRaises(MissingRequiredFieldException):
            request_to_project_accelerator_create_command(request)


class TestRequestToProjectAcceleratorUpdateCommand(SimpleTestCase):
    def test_valid_data_with_both_fields(self):
        request = Mock()
        request.data = {
            "name": "Updated Accelerator",
            "description": "Updated Description"
        }

        expected = ProjectAcceleratorUpdateCommand(
            name=AcceleratorName(value="Updated Accelerator"),
            description=Description(value="Updated Description")
        )
        result = request_to_project_accelerator_update_command(request)
        self.assertEqual(expected, result)

    def test_valid_data_with_name_only(self):
        request = Mock()
        request.data = {"name": "Updated Accelerator"}

        expected = ProjectAcceleratorUpdateCommand(
            name=AcceleratorName(value="Updated Accelerator"),
            description=None
        )
        result = request_to_project_accelerator_update_command(request)
        self.assertEqual(expected, result)

    def test_valid_data_with_description_only(self):
        request = Mock()
        request.data = {"description": "Updated Description"}

        expected = ProjectAcceleratorUpdateCommand(
            name=None,
            description=Description(value="Updated Description")
        )
        result = request_to_project_accelerator_update_command(request)
        self.assertEqual(expected, result)

    def test_empty_data(self):
        request = Mock()
        request.data = {}

        expected = ProjectAcceleratorUpdateCommand(
            name=None,
            description=None
        )
        result = request_to_project_accelerator_update_command(request)
        self.assertEqual(expected, result)
