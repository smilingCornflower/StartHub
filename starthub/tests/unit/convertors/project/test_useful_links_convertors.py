from dataclasses import dataclass
from unittest.mock import Mock

from django.test import SimpleTestCase
from domain.exceptions.validation import MissingRequiredFieldException
from domain.value_objects.project.useful_link import UsefulLinkCreateCommand, UsefulLinkName, UsefulLinkUpdateCommand
from presentation.request_converters.project.useful_link import (
    request_to_useful_link_create_command,
    request_to_useful_link_update_command,
)


@dataclass
class ValidUsefulLinkData:
    name = "Test Useful Link"
    url = "https://example.com/test"

    name_field = "name"
    url_field = "url"

    def to_dict(self):
        return {
            self.name_field: self.name,
            self.url_field: self.url,
        }


class TestRequestToUsefulLinkCreateCommand(SimpleTestCase):
    def setUp(self):
        self.valid_dataclass = ValidUsefulLinkData()

    def test_valid_data(self):
        request = Mock()
        request.data = self.valid_dataclass.to_dict()

        expected = UsefulLinkCreateCommand(
            name=UsefulLinkName(value=self.valid_dataclass.name), url=self.valid_dataclass.url
        )
        result = request_to_useful_link_create_command(request)
        self.assertEqual(expected, result)

    def test_missing_name_field(self):
        request = Mock()
        data = self.valid_dataclass.to_dict()
        del data[self.valid_dataclass.name_field]
        request.data = data

        with self.assertRaises(MissingRequiredFieldException):
            request_to_useful_link_create_command(request)

    def test_missing_url_field(self):
        request = Mock()
        data = self.valid_dataclass.to_dict()
        del data[self.valid_dataclass.url_field]
        request.data = data

        with self.assertRaises(MissingRequiredFieldException):
            request_to_useful_link_create_command(request)


class TestRequestToUsefulLinkUpdateCommand(SimpleTestCase):
    def setUp(self):
        self.valid_dataclass = ValidUsefulLinkData()

    def test_valid_data_with_both_fields(self):
        request = Mock()
        request.data = self.valid_dataclass.to_dict()

        expected = UsefulLinkUpdateCommand(
            name=UsefulLinkName(value=self.valid_dataclass.name), url=self.valid_dataclass.url
        )
        result = request_to_useful_link_update_command(request)
        self.assertEqual(expected, result)

    def test_valid_data_with_name_only(self):
        request = Mock()
        request.data = {self.valid_dataclass.name_field: self.valid_dataclass.name}

        expected = UsefulLinkUpdateCommand(name=UsefulLinkName(value=self.valid_dataclass.name), url=None)
        result = request_to_useful_link_update_command(request)
        self.assertEqual(expected, result)

    def test_valid_data_with_url_only(self):
        request = Mock()
        request.data = {self.valid_dataclass.url_field: self.valid_dataclass.url}

        expected = UsefulLinkUpdateCommand(name=None, url=self.valid_dataclass.url)
        result = request_to_useful_link_update_command(request)
        self.assertEqual(expected, result)

    def test_empty_data(self):
        request = Mock()
