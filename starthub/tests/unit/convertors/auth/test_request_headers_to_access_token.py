from dataclasses import dataclass

from django.test import SimpleTestCase
from domain.exceptions.validation import MissingRequiredFieldException
from domain.value_objects.auth_management.token import AccessTokenVo
from presentation.request_converters.user_management.auth import request_headers_to_access_token


@dataclass
class ValidAccessTokenData:
    access_token = "valid_access_token_123"
    authorization_header = "Bearer valid_access_token_123"

    authorization_field = "Authorization"

    def to_dict(self):
        return {
            self.authorization_field: self.authorization_header,
        }


class TestRequestHeadersToAccessToken(SimpleTestCase):
    def setUp(self):
        self.data = ValidAccessTokenData()

    def test_valid_data(self):
        headers = self.data.to_dict()

        expected = AccessTokenVo(value=self.data.access_token)

        result = request_headers_to_access_token(headers)
        self.assertEqual(expected, result)

    def test_invalid_data(self):
        headers = {self.data.authorization_field: "Invalid headers"}
        with self.assertRaises(MissingRequiredFieldException):  # Missing Bearer Token
            request_headers_to_access_token(headers)

    def test_missing_authorization_header(self):
        headers = {}

        with self.assertRaises(MissingRequiredFieldException):
            request_headers_to_access_token(headers)
