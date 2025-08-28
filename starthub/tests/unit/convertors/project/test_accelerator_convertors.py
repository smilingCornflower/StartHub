from dataclasses import dataclass
from unittest.mock import Mock

from django.test import SimpleTestCase
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


@dataclass
class ValidAcceleratorData:
    name = "Test Accelerator"
    description = "Test Description"

    name_field = "name"
    description_field = "description"

    def to_dict(self):
        return {
            self.name_field: self.name,
            self.description_field: self.description,
        }


class TestRequestToProjectAcceleratorCreateCommand(SimpleTestCase):
    def setUp(self):
        self.valid_dataclass = ValidAcceleratorData()

    def test_valid_data(self):
        request = Mock()
        request.data = self.valid_dataclass.to_dict()

        expected = ProjectAcceleratorCreateCommand(
            name=AcceleratorName(value=self.valid_dataclass.name),
            description=Description(value=self.valid_dataclass.description),
        )

        result = request_to_project_accelerator_create_command(request)
        self.assertEqual(expected, result)

    def test_missing_name_field(self):
        request = Mock()
        data = self.valid_dataclass.to_dict()
        del data[self.valid_dataclass.name_field]
        request.data = data

        with self.assertRaises(MissingRequiredFieldException):
            request_to_project_accelerator_create_command(request)

    def test_missing_description_field(self):
        request = Mock()
        data = self.valid_dataclass.to_dict()
        del data[self.valid_dataclass.description_field]
        request.data = data

        with self.assertRaises(MissingRequiredFieldException):
            request_to_project_accelerator_create_command(request)


class TestRequestToProjectAcceleratorUpdateCommand(SimpleTestCase):
    def setUp(self):
        self.valid_dataclass = ValidAcceleratorData()

    def test_valid_data_with_both_fields(self):
        request = Mock()
        request.data = self.valid_dataclass.to_dict()

        expected = ProjectAcceleratorUpdateCommand(
            name=AcceleratorName(value=self.valid_dataclass.name),
            description=Description(value=self.valid_dataclass.description),
        )
        result = request_to_project_accelerator_update_command(request)
        self.assertEqual(expected, result)

    def test_valid_data_with_name_only(self):
        request = Mock()
        request.data = {self.valid_dataclass.name_field: self.valid_dataclass.name}

        expected = ProjectAcceleratorUpdateCommand(
            name=AcceleratorName(value=self.valid_dataclass.name), description=None
        )
        result = request_to_project_accelerator_update_command(request)
        self.assertEqual(expected, result)

    def test_valid_data_with_description_only(self):
        request = Mock()
        request.data = {self.valid_dataclass.description_field: self.valid_dataclass.description}

        expected = ProjectAcceleratorUpdateCommand(
            name=None, description=Description(value=self.valid_dataclass.description)
        )
        result = request_to_project_accelerator_update_command(request)
        self.assertEqual(expected, result)

    def test_empty_data(self):
        request = Mock()
        request.data = {}

        expected = ProjectAcceleratorUpdateCommand(name=None, description=None)
        result = request_to_project_accelerator_update_command(request)
        self.assertEqual(expected, result)
