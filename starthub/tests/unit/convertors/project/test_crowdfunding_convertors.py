from dataclasses import dataclass
from unittest.mock import Mock

from django.test import SimpleTestCase
from domain.exceptions.validation import MissingRequiredFieldException
from domain.value_objects.project.crowdfunding import (
    ProjectCrowdfundingAmount,
    ProjectCrowdfundingCreateCommand,
    ProjectCrowdfundingName,
    ProjectCrowdfundingUpdateCommand,
)
from presentation.request_converters.project.crowdfunding import (
    request_to_project_crowdfunding_create_command,
    request_to_project_crowdfunding_update_command,
)


@dataclass
class ValidCrowdfundingData:
    name = "Test Crowdfunding"
    amount = 50000
    name_field = "name"
    amount_field = "amount"

    def to_dict(self):
        return {self.name_field: self.name, self.amount_field: self.amount}


class TestRequestToProjectCrowdfundingCreateCommand(SimpleTestCase):
    def setUp(self):
        self.valid_dataclass = ValidCrowdfundingData()

    def test_valid_data(self):
        request = Mock()
        request.data = self.valid_dataclass.to_dict()

        expected = ProjectCrowdfundingCreateCommand(
            name=ProjectCrowdfundingName(value=self.valid_dataclass.name),
            amount=ProjectCrowdfundingAmount(value=self.valid_dataclass.amount),
        )

        result = request_to_project_crowdfunding_create_command(request)
        self.assertEqual(expected, result)

    def test_missing_name_field(self):
        request = Mock()
        data = self.valid_dataclass.to_dict()
        del data[self.valid_dataclass.name_field]
        request.data = data

        with self.assertRaises(MissingRequiredFieldException):
            request_to_project_crowdfunding_create_command(request)

    def test_missing_amount_field(self):
        request = Mock()
        data = self.valid_dataclass.to_dict()
        del data[self.valid_dataclass.amount_field]
        request.data = data

        with self.assertRaises(MissingRequiredFieldException):
            request_to_project_crowdfunding_create_command(request)


class TestRequestToProjectCrowdfundingUpdateCommand(SimpleTestCase):
    def setUp(self):
        self.valid_dataclass = ValidCrowdfundingData()

    def test_valid_data_with_all_fields(self):
        request = Mock()
        request.data = self.valid_dataclass.to_dict()

        expected = ProjectCrowdfundingUpdateCommand(
            name=ProjectCrowdfundingName(value=self.valid_dataclass.name),
            amount=ProjectCrowdfundingAmount(value=self.valid_dataclass.amount),
        )
        result = request_to_project_crowdfunding_update_command(request)
        self.assertEqual(expected, result)

    def test_valid_data_with_name_only(self):
        request = Mock()
        request.data = {self.valid_dataclass.name_field: self.valid_dataclass.name}

        expected = ProjectCrowdfundingUpdateCommand(
            name=ProjectCrowdfundingName(value=self.valid_dataclass.name), amount=None
        )
        result = request_to_project_crowdfunding_update_command(request)
        self.assertEqual(expected, result)

    def test_valid_data_with_amount_only(self):
        request = Mock()
        request.data = {self.valid_dataclass.amount_field: self.valid_dataclass.amount}

        expected = ProjectCrowdfundingUpdateCommand(
            name=None, amount=ProjectCrowdfundingAmount(value=self.valid_dataclass.amount)
        )
        result = request_to_project_crowdfunding_update_command(request)
        self.assertEqual(expected, result)

    def test_empty_data(self):
        request = Mock()
        request.data = {}

        expected = ProjectCrowdfundingUpdateCommand(name=None, amount=None)
        result = request_to_project_crowdfunding_update_command(request)
        self.assertEqual(expected, result)
