from dataclasses import dataclass
from unittest.mock import MagicMock

from django.test import SimpleTestCase
from domain.exceptions.validation import MissingRequiredFieldException
from domain.value_objects.auth_management.token import AccessTokenVo
from presentation.request_converters.user_management.auth import request_to_access_token


@dataclass
class ValidAccessTokenData:
    access_token = "valid_access_token_123"
    authorization_header = "Bearer valid_access_token_123"

    authorization_field = "Authorization"

    def to_dict(self):
        return {
            self.authorization_field: self.authorization_header,
        }


class TestRequestToAccessToken(SimpleTestCase):
    def setUp(self):
        self.data = ValidAccessTokenData()

    def test_valid_data(self):
        headers = self.data.to_dict()

        expected = AccessTokenVo(value=self.data.access_token)

        request = MagicMock()
        request.headers = headers
        result = request_to_access_token(request=request)

        self.assertEqual(expected, result)

    def test_invalid_data(self):
        headers = {self.data.authorization_field: "Invalid headers"}
        request = MagicMock()
        request.headers = headers
        with self.assertRaises(MissingRequiredFieldException):  # Missing Bearer Token
            request_to_access_token(request=request)

    def test_missing_authorization_header(self):
        headers = {}
        request = MagicMock()
        request.headers = headers

        with self.assertRaises(MissingRequiredFieldException):
            request_to_access_token(request=request)
