from dataclasses import dataclass
from unittest.mock import Mock

from django.test import SimpleTestCase
from domain.exceptions.validation import MissingRequiredFieldException
from domain.value_objects.project.government_grant import (
    ProjectGovernmentGrantAmount,
    ProjectGovernmentGrantCreateCommand,
    ProjectGoverntmentGrantUpdateCommand,
    ProjectGrantName,
    ProjectGrantOrganizationName,
)
from presentation.request_converters.project.government_grant import (
    request_to_project_government_grant_create_command,
    request_to_project_government_grant_update_command,
)


@dataclass
class ValidGovernmentGrantData:
    grant_name = "Test Grant"
    organization_name = "Test Organization"
    amount = 75000

    grant_name_field = "grant_name"
    organization_name_field = "organization_name"
    amount_field = "amount"

    def to_dict(self):
        return {
            self.grant_name_field: self.grant_name,
            self.organization_name_field: self.organization_name,
            self.amount_field: self.amount,
        }


class TestRequestToProjectGovernmentGrantCreateCommand(SimpleTestCase):
    def setUp(self):
        self.valid_dataclass = ValidGovernmentGrantData()

    def test_valid_data(self):
        request = Mock()
        request.data = self.valid_dataclass.to_dict()

        expected = ProjectGovernmentGrantCreateCommand(
            grant_name=ProjectGrantName(value=self.valid_dataclass.grant_name),
            organization_name=ProjectGrantOrganizationName(value=self.valid_dataclass.organization_name),
            amount=ProjectGovernmentGrantAmount(value=self.valid_dataclass.amount),
        )

        result = request_to_project_government_grant_create_command(request)
        self.assertEqual(expected, result)

    def test_missing_grant_name_field(self):
        request = Mock()
        data = self.valid_dataclass.to_dict()
        del data[self.valid_dataclass.grant_name_field]
        request.data = data

        with self.assertRaises(MissingRequiredFieldException):
            request_to_project_government_grant_create_command(request)

    def test_missing_organization_name_field(self):
        request = Mock()
        data = self.valid_dataclass.to_dict()
        del data[self.valid_dataclass.organization_name_field]
        request.data = data

        with self.assertRaises(MissingRequiredFieldException):
            request_to_project_government_grant_create_command(request)

    def test_missing_amount_field(self):
        request = Mock()
        data = self.valid_dataclass.to_dict()
        del data[self.valid_dataclass.amount_field]
        request.data = data

        with self.assertRaises(MissingRequiredFieldException):
            request_to_project_government_grant_create_command(request)


class TestRequestToProjectGovernmentGrantUpdateCommand(SimpleTestCase):
    def setUp(self):
        self.valid_dataclass = ValidGovernmentGrantData()

    def test_valid_data_with_all_fields(self):
        request = Mock()
        request.data = self.valid_dataclass.to_dict()

        expected = ProjectGoverntmentGrantUpdateCommand(
            grant_name=ProjectGrantName(value=self.valid_dataclass.grant_name),
            organization_name=ProjectGrantOrganizationName(value=self.valid_dataclass.organization_name),
            amount=ProjectGovernmentGrantAmount(value=self.valid_dataclass.amount),
        )
        result = request_to_project_government_grant_update_command(request)
        self.assertEqual(expected, result)

    def test_valid_data_with_grant_name_only(self):
        request = Mock()
        request.data = {self.valid_dataclass.grant_name_field: self.valid_dataclass.grant_name}

        expected = ProjectGoverntmentGrantUpdateCommand(
            grant_name=ProjectGrantName(value=self.valid_dataclass.grant_name), organization_name=None, amount=None
        )
        result = request_to_project_government_grant_update_command(request)
        self.assertEqual(expected, result)

    def test_valid_data_with_organization_name_only(self):
        request = Mock()
        request.data = {self.valid_dataclass.organization_name_field: self.valid_dataclass.organization_name}

        expected = ProjectGoverntmentGrantUpdateCommand(
            grant_name=None,
            organization_name=ProjectGrantOrganizationName(value=self.valid_dataclass.organization_name),
            amount=None,
        )
        result = request_to_project_government_grant_update_command(request)
        self.assertEqual(expected, result)

    def test_valid_data_with_amount_only(self):
        request = Mock()
        request.data = {self.valid_dataclass.amount_field: self.valid_dataclass.amount}

        expected = ProjectGoverntmentGrantUpdateCommand(
            grant_name=None,
            organization_name=None,
            amount=ProjectGovernmentGrantAmount(value=self.valid_dataclass.amount),
        )
        result = request_to_project_government_grant_update_command(request)
        self.assertEqual(expected, result)

    def test_empty_data(self):
        request = Mock()
        request.data = {}

        expected = ProjectGoverntmentGrantUpdateCommand(grant_name=None, organization_name=None, amount=None)
        result = request_to_project_government_grant_update_command(request)
        self.assertEqual(expected, result)
