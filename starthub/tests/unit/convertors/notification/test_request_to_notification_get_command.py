from dataclasses import dataclass
from unittest.mock import Mock

from django.http import QueryDict
from django.test import SimpleTestCase
from domain.exceptions.validation import ValidationException
from domain.value_objects.notification import NotificationGetCommand
from presentation.request_converters.notification import request_to_notification_get_command
from rest_framework.request import Request
from tests.utils import check_raises


@dataclass
class NotificationGetData:
    is_read_true = "true"
    is_read_false = "false"
    is_read_invalid = "invalid"

    is_read_field = "is_read"


class TestRequestToNotificationGetCommand(SimpleTestCase):
    def setUp(self):
        self.data = NotificationGetData()

    @staticmethod
    def apply_function(query_string):
        request = Mock(spec=Request)
        request.query_params = QueryDict(query_string)
        return request_to_notification_get_command(request)

    def test_no_query_params(self):
        expected = NotificationGetCommand(is_read=None)

        result = self.apply_function("")
        self.assertEqual(expected, result)

    def test_is_read_true(self):
        expected = NotificationGetCommand(is_read=True)

        result = self.apply_function(f"{self.data.is_read_field}={self.data.is_read_true}")
        self.assertEqual(expected, result)

    def test_is_read_false(self):
        expected = NotificationGetCommand(is_read=False)

        result = self.apply_function(f"{self.data.is_read_field}={self.data.is_read_false}")
        self.assertEqual(expected, result)

    def test_invalid_is_read_value(self):
        exc = ValidationException
        check_raises(request_to_notification_get_command, exc)
        with self.assertRaises(exc):
            self.apply_function(f"{self.data.is_read_field}={self.data.is_read_invalid}")
