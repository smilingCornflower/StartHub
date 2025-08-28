from dataclasses import dataclass

from django.test import SimpleTestCase
from domain.exceptions.validation import MissingRequiredFieldException
from domain.value_objects.auth_management.token import AnonymousTokenVo
from presentation.request_converters.user_management.auth import request_headers_to_anonymous_token


@dataclass
class ValidAnonymousTokenData:
    anonymous_token = "anon:anonymous_token_123"
    authorization_header = f"Bearer anon:anonymous_token_123"

    authorization_field = "Authorization"

    def to_dict(self):
        return {
            self.authorization_field: self.authorization_header,
        }


class TestRequestHeadersToAnonymousToken(SimpleTestCase):
    def setUp(self):
        self.valid_dataclass = ValidAnonymousTokenData()

    def test_valid_data(self):
        headers = self.valid_dataclass.to_dict()

        expected = AnonymousTokenVo(value=self.valid_dataclass.anonymous_token)

        result = request_headers_to_anonymous_token(headers)
        self.assertEqual(expected, result)

    def test_missing_authorization_header(self):
        headers = {}

        with self.assertRaises(MissingRequiredFieldException):
            request_headers_to_anonymous_token(headers)
