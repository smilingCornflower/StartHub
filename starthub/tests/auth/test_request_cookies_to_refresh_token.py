from django.test import SimpleTestCase
from domain.exceptions.validation import MissingRequiredFieldException
from domain.value_objects.auth_management.token import RefreshTokenVo
from presentation.request_converters.user_management.auth import request_cookies_to_refresh_token


class TestRequestCookiesToRefreshToken(SimpleTestCase):
    def test_valid_data(self):
        cookies = {"refresh_token": "valid_token_123"}

        expected = RefreshTokenVo(value="valid_token_123")

        result = request_cookies_to_refresh_token(cookies)
        self.assertEqual(expected, result)

    def test_missing_refresh_token(self):
        cookies = {}

        with self.assertRaises(MissingRequiredFieldException):
            request_cookies_to_refresh_token(cookies)
