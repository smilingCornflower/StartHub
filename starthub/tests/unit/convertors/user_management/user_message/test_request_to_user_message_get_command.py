from unittest.mock import Mock

from django.http import QueryDict
from django.test import SimpleTestCase
from domain.exceptions.validation import ValidationException
from domain.value_objects.user_management.user_message import UserMessageGetCommand, UserMessageOrderByEnum
from presentation.request_converters.user_management.user_message import request_to_user_message_get_command
from rest_framework.request import Request


class TestRequestToUserMessageGetCommand(SimpleTestCase):
    def test_no_query_params(self):
        request = Mock(spec=Request)
        request.query_params = QueryDict()

        expected = UserMessageGetCommand(
            is_read=None,
            order_by=None,
        )

        result = request_to_user_message_get_command(request)
        self.assertEqual(expected, result)

    def test_is_read_true(self):
        request = Mock(spec=Request)
        request.query_params = QueryDict("is_read=true")

        expected = UserMessageGetCommand(
            is_read=True,
            order_by=None,
        )

        result = request_to_user_message_get_command(request)
        self.assertEqual(expected, result)

    def test_is_read_false(self):
        request = Mock(spec=Request)
        request.query_params = QueryDict("is_read=false")

        expected = UserMessageGetCommand(
            is_read=False,
            order_by=None,
        )

        result = request_to_user_message_get_command(request)
        self.assertEqual(expected, result)

    def test_invalid_is_read_value(self):
        request = Mock(spec=Request)
        request.query_params = QueryDict("is_read=invalid")

        with self.assertRaises(ValidationException) as context:
            request_to_user_message_get_command(request)

        self.assertIn("Invalid value for is_read: invalid", str(context.exception))

    def test_order_by_created_at_asc(self):
        request = Mock(spec=Request)
        request.query_params = QueryDict("order_by=created_at")

        expected = UserMessageGetCommand(
            is_read=None,
            order_by=UserMessageOrderByEnum.CREATED_AT_ASC,
        )

        result = request_to_user_message_get_command(request)
        self.assertEqual(expected, result)

    def test_order_by_created_at_desc(self):
        request = Mock(spec=Request)
        request.query_params = QueryDict("order_by=-created_at")

        expected = UserMessageGetCommand(
            is_read=None,
            order_by=UserMessageOrderByEnum.CREATED_AT_DESC,
        )

        result = request_to_user_message_get_command(request)
        self.assertEqual(expected, result)

    def test_invalid_order_by(self):
        request = Mock(spec=Request)
        request.query_params = QueryDict("order_by=invalid_field")

        with self.assertRaises(ValidationException) as context:
            request_to_user_message_get_command(request)

    def test_both_params_valid(self):
        request = Mock(spec=Request)
        request.query_params = QueryDict("is_read=true&order_by=created_at")

        expected = UserMessageGetCommand(
            is_read=True,
            order_by=UserMessageOrderByEnum.CREATED_AT_ASC,
        )

        result = request_to_user_message_get_command(request)
        self.assertEqual(expected, result)
