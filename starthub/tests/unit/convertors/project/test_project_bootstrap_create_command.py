from dataclasses import dataclass
from unittest.mock import Mock

from django.test import SimpleTestCase
from domain.exceptions.validation import MissingRequiredFieldException
from domain.value_objects.common import Description
from domain.value_objects.project.bootstrap import ProjectBootstrapCreateCommand, ProjectBootstrapUpdateCommand
from presentation.request_converters.project.bootstrap import (
    request_to_project_bootstrap_create_command,
    request_to_project_bootstrap_update_command,
)


@dataclass
class ValidBootstrapData:
    description = "Test Bootstrap Description"
    description_field = "description"

    def to_dict(self):
        return {
            self.description_field: self.description,
        }


class TestRequestToProjectBootstrapCreateCommand(SimpleTestCase):
    def setUp(self):
        self.valid_dataclass = ValidBootstrapData()

    def test_valid_data(self):
        request = Mock()
        request.data = self.valid_dataclass.to_dict()

        expected = ProjectBootstrapCreateCommand(description=Description(value=self.valid_dataclass.description))
        result = request_to_project_bootstrap_create_command(request)
        self.assertEqual(expected, result)

    def test_missing_description_field(self):
        request = Mock()
        data = self.valid_dataclass.to_dict()
        del data[self.valid_dataclass.description_field]
        request.data = data

        with self.assertRaises(MissingRequiredFieldException):
            request_to_project_bootstrap_create_command(request)


class TestRequestToProjectBootstrapUpdateCommand(SimpleTestCase):
    def setUp(self):
        self.valid_dataclass = ValidBootstrapData()

    def test_valid_data_with_description(self):
        request = Mock()
        request.data = self.valid_dataclass.to_dict()

        expected = ProjectBootstrapUpdateCommand(description=Description(value=self.valid_dataclass.description))
        result = request_to_project_bootstrap_update_command(request)
        self.assertEqual(expected, result)

    def test_empty_data(self):
        request = Mock()
        request.data = {}

        expected = ProjectBootstrapUpdateCommand(description=None)
        result = request_to_project_bootstrap_update_command(request)
        self.assertEqual(expected, result)
