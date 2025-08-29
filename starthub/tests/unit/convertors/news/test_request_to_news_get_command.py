from dataclasses import dataclass
from datetime import date
from unittest.mock import Mock

from django.http import QueryDict
from django.test import SimpleTestCase
from domain.value_objects.news_management.news import NewsGetCommand
from presentation.request_converters.news import request_to_news_get_command
from rest_framework.request import Request


@dataclass
class NewsGetTestData:
    published_at_start = "2024-01-01"
    published_at_end = "2024-12-31"

    published_at_start_field = "published_at_start"
    published_at_end_field = "published_at_end"


class TestRequestToNewsGetCommand(SimpleTestCase):
    def setUp(self):
        self.data = NewsGetTestData()

    def apply_function(self, query_string):
        request = Mock(spec=Request)
        request.query_params = QueryDict(query_string)
        return request_to_news_get_command(request)

    def test_no_query_params(self):
        expected = NewsGetCommand(
            published_at_start=None,
            published_at_end=None,
        )

        result = self.apply_function("")
        self.assertEqual(expected, result)

    def test_with_published_at_start_only(self):
        expected = NewsGetCommand(
            published_at_start=date.fromisoformat(self.data.published_at_start),
            published_at_end=None,
        )

        result = self.apply_function(f"{self.data.published_at_start_field}={self.data.published_at_start}")
        self.assertEqual(expected, result)

    def test_with_published_at_end_only(self):
        expected = NewsGetCommand(
            published_at_start=None,
            published_at_end=date.fromisoformat(self.data.published_at_end),
        )

        result = self.apply_function(f"{self.data.published_at_end_field}={self.data.published_at_end}")
        self.assertEqual(expected, result)

    def test_with_both_dates(self):
        expected = NewsGetCommand(
            published_at_start=date.fromisoformat(self.data.published_at_start),
            published_at_end=date.fromisoformat(self.data.published_at_end),
        )

        query_string = (
            f"{self.data.published_at_start_field}={self.data.published_at_start}&"
            f"{self.data.published_at_end_field}={self.data.published_at_end}"
        )

        result = self.apply_function(query_string)
        self.assertEqual(expected, result)
