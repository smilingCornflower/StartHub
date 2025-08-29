from dataclasses import dataclass
from unittest.mock import Mock

from django.test import SimpleTestCase
from domain.exceptions.validation import MissingRequiredFieldException, ValidationException
from domain.value_objects.news_management.news import NewsTagEnum
from presentation.request_converters.news import request_to_news_tag_name
from rest_framework.request import Request
from tests.common.check_raises import check_raises


@dataclass
class NewsTagTestData:
    valid_tag_name = "world"
    invalid_tag_name = "INVALID"
    non_string_tag = 123

    tag_name_field = "tag_name"


class TestRequestToNewsTagName(SimpleTestCase):
    def setUp(self):
        self.data = NewsTagTestData()

    def apply_function(self, request_data):
        request = Mock(spec=Request)
        request.data = request_data
        return request_to_news_tag_name(request)

    def test_valid_tag_name(self):
        data = {self.data.tag_name_field: self.data.valid_tag_name}
        expected = NewsTagEnum(self.data.valid_tag_name)

        result = self.apply_function(data)
        self.assertEqual(expected, result)

    def test_missing_tag_name(self):
        data = {}

        with self.assertRaises(MissingRequiredFieldException):
            self.apply_function(data)

    def test_non_string_tag_name(self):
        data = {self.data.tag_name_field: self.data.non_string_tag}

        exc = TypeError

        check_raises(request_to_news_tag_name, exc)
        with self.assertRaises(exc):
            self.apply_function(data)

    def test_invalid_tag_name(self):
        data = {self.data.tag_name_field: self.data.invalid_tag_name}

        exc = ValidationException

        check_raises(request_to_news_tag_name, exc)
        with self.assertRaises(exc):
            self.apply_function(data)
