from dataclasses import dataclass

from django.test import SimpleTestCase
from domain.exceptions.validation import MissingRequiredFieldException
from domain.value_objects.auth_management.token import AccessTokenVo, AnonymousTokenVo
from presentation.request_converters.user_management.auth import request_headers_to_access_or_anonymous_token


@dataclass
class ValidTokenData:
    anonymous_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhbm9uOmJhYWEzMDc3LTZjODQtNDkzMS04YzIzLWUyYmNmZmRjYmUwOSIsImlhdCI6MTc1NjM5Njc4MiwiZXhwIjoxNzU4OTg4NzgyLCJ0eXBlIjoiYW5vbnltb3VzIn0.iLBJV6VTMR8KrB8iTk5uM37BZJkMPDXK6MDMXDGLvFQ"
    access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyIiwicm9sZXMiOlsidXNlciJdLCJlbWFpbCI6InRlc3RAZXhhbXBsZS5jb20iLCJmaXJzdF9uYW1lIjoiZGVmYXVsdCBmaXJzdCBuYW1lIiwibGFzdF9uYW1lIjoiZGVmYXVsdCBsYXN0IG5hbWUiLCJpYXQiOjE3NTYzOTY3NDcsImV4cCI6MTc1NjM5NzY0NywidHlwZSI6ImFjY2VzcyJ9.ji3-4BcNgiGiFhfmACoYi8Kj_uV1t_n7oFCuhsXFxlo"

    authorization_field = "Authorization"

    def create_anonymous_headers(self):
        return {
            self.authorization_field: f"Bearer {self.anonymous_token}",
        }

    def create_access_headers(self):
        return {
            self.authorization_field: f"Bearer {self.access_token}",
        }


class TestRequestHeadersToAccessOrAnonymousToken(SimpleTestCase):
    def setUp(self):
        self.valid_dataclass = ValidTokenData()

    def test_returns_anonymous_token(self):
        headers = self.valid_dataclass.create_anonymous_headers()

        result = request_headers_to_access_or_anonymous_token(headers)

        self.assertIsInstance(result, AnonymousTokenVo)

    def test_returns_access_token(self):
        headers = self.valid_dataclass.create_access_headers()

        result = request_headers_to_access_or_anonymous_token(headers)

        self.assertIsInstance(result, AccessTokenVo)

    def test_missing_authorization_header(self):
        headers = {}

        with self.assertRaises(MissingRequiredFieldException):
            request_headers_to_access_or_anonymous_token(headers)
