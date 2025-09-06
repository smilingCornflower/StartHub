from dataclasses import dataclass
from unittest.mock import MagicMock

from django.test import SimpleTestCase
from domain.exceptions.validation import MissingRequiredFieldException
from domain.value_objects.auth_management.token import AnonymousTokenVo
from presentation.request_converters.user_management.auth import request_to_anonymous_token


@dataclass
class ValidAnonymousTokenData:
    anonymous_token = "anon:anonymous_token_123"
    authorization_header = "Bearer anon:anonymous_token_123"

    authorization_field = "Authorization"

    def to_dict(self):
        return {
            self.authorization_field: self.authorization_header,
        }


class TestRequestHeadersToAnonymousToken(SimpleTestCase):
    def setUp(self):
        self.data = ValidAnonymousTokenData()

    def test_valid_data(self):
        headers = self.data.to_dict()

        expected = AnonymousTokenVo(value=self.data.anonymous_token)
        request = MagicMock()
        request.headers = headers
        result = request_to_anonymous_token(request=request)

        self.assertEqual(expected, result)

    def test_invalid_data(self):
        headers = {self.data.authorization_field: "Invalid headers"}
        request = MagicMock()
        request.headers = headers
        with self.assertRaises(MissingRequiredFieldException):  # Missing Bearer Token
            request_to_anonymous_token(request=request)

    def test_missing_authorization_header(self):
        headers = {}

        request = MagicMock()
        request.headers = headers
        with self.assertRaises(MissingRequiredFieldException):
            request_to_anonymous_token(request=request)
