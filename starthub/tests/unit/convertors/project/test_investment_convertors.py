from dataclasses import dataclass
from unittest.mock import Mock

from django.test import SimpleTestCase
from domain.exceptions.validation import MissingRequiredFieldException
from domain.value_objects.common import PhoneNumber, SocialLink
from domain.value_objects.project.investment import (
    ProjectInvestmentAmount,
    ProjectInvestmentCreateCommand,
    ProjectInvestmentOrganizationName,
    ProjectInvestmentUpdateCommand,
)
from presentation.request_converters.project.investment import (
    request_to_project_investment_create_command,
    request_to_project_investment_update_command,
)


@dataclass
class ValidInvestmentData:
    organization_name = "Test Investment Org"
    amount = 250000.0
    social_links = {"twitter": "https://twitter.com/test", "linkedin": "https://linkedin.com/test"}
    phone_numbers = ["+77001234567", "+44-20-7946-0958"]

    organization_name_field = "organization_name"
    amount_field = "amount"
    social_links_field = "social_links"
    phone_numbers_field = "phone_numbers"

    def to_dict(self):
        return {
            self.organization_name_field: self.organization_name,
            self.amount_field: self.amount,
            self.social_links_field: self.social_links,
            self.phone_numbers_field: self.phone_numbers,
        }


class TestRequestToProjectInvestmentCreateCommand(SimpleTestCase):
    def setUp(self):
        self.valid_dataclass = ValidInvestmentData()

    def test_valid_data(self):
        request = Mock()
        request.data = self.valid_dataclass.to_dict()

        expected = ProjectInvestmentCreateCommand(
            organization_name=ProjectInvestmentOrganizationName(value=self.valid_dataclass.organization_name),
            amount=ProjectInvestmentAmount(value=self.valid_dataclass.amount),
            social_links=[SocialLink(platform=k, link=v) for k, v in self.valid_dataclass.social_links.items()],
            phone_numbers=[PhoneNumber(value=i) for i in self.valid_dataclass.phone_numbers],
        )

        result = request_to_project_investment_create_command(request)
        self.assertEqual(expected, result)

    def test_missing_organization_name_field(self):
        request = Mock()
        data = self.valid_dataclass.to_dict()
        del data[self.valid_dataclass.organization_name_field]
        request.data = data

        with self.assertRaises(MissingRequiredFieldException):
            request_to_project_investment_create_command(request)

    def test_missing_amount_field(self):
        request = Mock()
        data = self.valid_dataclass.to_dict()
        del data[self.valid_dataclass.amount_field]
        request.data = data

        with self.assertRaises(MissingRequiredFieldException):
            request_to_project_investment_create_command(request)

    def test_missing_social_links_field(self):
        request = Mock()
        data = self.valid_dataclass.to_dict()
        del data[self.valid_dataclass.social_links_field]
        request.data = data

        with self.assertRaises(MissingRequiredFieldException):
            request_to_project_investment_create_command(request)

    def test_missing_phone_numbers_field(self):
        request = Mock()
        data = self.valid_dataclass.to_dict()
        del data[self.valid_dataclass.phone_numbers_field]
        request.data = data

        with self.assertRaises(MissingRequiredFieldException):
            request_to_project_investment_create_command(request)


class TestRequestToProjectInvestmentUpdateCommand(SimpleTestCase):
    def setUp(self):
        self.valid_dataclass = ValidInvestmentData()

    def test_valid_data_with_all_fields(self):
        request = Mock()
        request.data = self.valid_dataclass.to_dict()

        expected = ProjectInvestmentUpdateCommand(
            organization_name=ProjectInvestmentOrganizationName(value=self.valid_dataclass.organization_name),
            amount=ProjectInvestmentAmount(value=self.valid_dataclass.amount),
            social_links=[SocialLink(platform=k, link=v) for k, v in self.valid_dataclass.social_links.items()],
        )
        result = request_to_project_investment_update_command(request)
        self.assertEqual(expected, result)

    def test_valid_data_with_organization_name_only(self):
        request = Mock()
        request.data = {self.valid_dataclass.organization_name_field: self.valid_dataclass.organization_name}

        expected = ProjectInvestmentUpdateCommand(
            organization_name=ProjectInvestmentOrganizationName(value=self.valid_dataclass.organization_name),
            amount=None,
            social_links=None,
        )
        result = request_to_project_investment_update_command(request)
        self.assertEqual(expected, result)

    def test_valid_data_with_amount_only(self):
        request = Mock()
        request.data = {self.valid_dataclass.amount_field: self.valid_dataclass.amount}

        expected = ProjectInvestmentUpdateCommand(
            organization_name=None, amount=ProjectInvestmentAmount(value=self.valid_dataclass.amount), social_links=None
        )
        result = request_to_project_investment_update_command(request)
        self.assertEqual(expected, result)

    def test_valid_data_with_social_links_only(self):
        request = Mock()
        request.data = {self.valid_dataclass.social_links_field: self.valid_dataclass.social_links}

        expected = ProjectInvestmentUpdateCommand(
            organization_name=None,
            amount=None,
            social_links=[SocialLink(platform=k, link=v) for k, v in self.valid_dataclass.social_links.items()],
        )
        result = request_to_project_investment_update_command(request)
        self.assertEqual(expected, result)

    def test_empty_data(self):
        request = Mock()
        request.data = {}

        expected = ProjectInvestmentUpdateCommand(organization_name=None, amount=None, social_links=None)
        result = request_to_project_investment_update_command(request)
        self.assertEqual(expected, result)
