from dataclasses import dataclass

from django.test import SimpleTestCase
from domain.exceptions.validation import MissingRequiredFieldException
from domain.value_objects.user_management.user import Email, RawPassword, UserCreatePayload
from presentation.request_converters.user_management.auth import request_data_to_user_create_payload


@dataclass
class ValidAuthData:
    email = "test@example.com"
    password = "SecurePassword123!"

    email_field = "email"
    password_field = "password"

    def to_dict(self):
        return {
            self.email_field: self.email,
            self.password_field: self.password,
        }


class TestRequestDataToUserCreatePayload(SimpleTestCase):
    def setUp(self):
        self.valid_dataclass = ValidAuthData()

    def test_valid_data(self):
        data = self.valid_dataclass.to_dict()

        expected = UserCreatePayload(
            email=Email(value=self.valid_dataclass.email), password=RawPassword(value=self.valid_dataclass.password)
        )

        result = request_data_to_user_create_payload(data)
        self.assertEqual(expected, result)

    def test_missing_email(self):
        data = self.valid_dataclass.to_dict()
        del data[self.valid_dataclass.email_field]

        with self.assertRaises(MissingRequiredFieldException):
            request_data_to_user_create_payload(data)

    def test_missing_password(self):
        data = self.valid_dataclass.to_dict()
        del data[self.valid_dataclass.password_field]

        with self.assertRaises(MissingRequiredFieldException):
            request_data_to_user_create_payload(data)
