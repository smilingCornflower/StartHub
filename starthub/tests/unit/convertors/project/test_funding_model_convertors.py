from dataclasses import dataclass
from unittest.mock import Mock

from django.test import SimpleTestCase
from domain.value_objects.project.funding_model import FundingModelUpdateCommand
from presentation.request_converters.project.funding_model import request_to_funding_model_update_command


@dataclass
class ValidFundingModelData:
    name = "Test Funding Model"
    description = "Test Description"
    recommended = True

    name_field = "name"
    description_field = "description"
    recommended_field = "recommended"

    def to_dict(self):
        return {
            self.name_field: self.name,
            self.description_field: self.description,
            self.recommended_field: self.recommended,
        }


class TestRequestToFundingModelUpdateCommand(SimpleTestCase):
    def setUp(self):
        self.valid_dataclass = ValidFundingModelData()

    def test_valid_data_with_all_fields(self):
        request = Mock()
        request.data = self.valid_dataclass.to_dict()

        expected = FundingModelUpdateCommand(
            name=self.valid_dataclass.name,
            description=self.valid_dataclass.description,
            recommended=self.valid_dataclass.recommended,
        )
        result = request_to_funding_model_update_command(request)
        self.assertEqual(expected, result)

    def test_valid_data_with_name_only(self):
        request = Mock()
        request.data = {self.valid_dataclass.name_field: self.valid_dataclass.name}

        expected = FundingModelUpdateCommand(name=self.valid_dataclass.name, description=None, recommended=None)
        result = request_to_funding_model_update_command(request)
        self.assertEqual(expected, result)

    def test_valid_data_with_description_only(self):
        request = Mock()
        request.data = {self.valid_dataclass.description_field: self.valid_dataclass.description}

        expected = FundingModelUpdateCommand(name=None, description=self.valid_dataclass.description, recommended=None)
        result = request_to_funding_model_update_command(request)
        self.assertEqual(expected, result)

    def test_valid_data_with_recommended_only(self):
        request = Mock()
        request.data = {self.valid_dataclass.recommended_field: self.valid_dataclass.recommended}

        expected = FundingModelUpdateCommand(name=None, description=None, recommended=self.valid_dataclass.recommended)
        result = request_to_funding_model_update_command(request)
        self.assertEqual(expected, result)

    def test_empty_data(self):
        request = Mock()
        request.data = {}

        expected = FundingModelUpdateCommand(name=None, description=None, recommended=None)
        result = request_to_funding_model_update_command(request)
        self.assertEqual(expected, result)
