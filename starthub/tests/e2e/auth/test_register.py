from django.test import TestCase
from django.urls import reverse
from domain.exceptions.auth import PasswordValidationException
from domain.exceptions.user import EmailAlreadyExistsException
from domain.exceptions.validation import (
    EmptyStringException,
    FirstNameIsTooLongException,
    InvalidEmailException,
    LastNameIsTooLongException,
    MissingRequiredFieldException,
)
from domain.models.user import User
from loguru import logger
from presentation.constants import SUCCESS
from presentation.response_factories.common import RegistrationErrorResponseFactory
from pydantic import ValidationError
from rest_framework.test import APIClient


class TestRegister(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.register_url = reverse("register")
        self.valid_data = {
            "first_name": "first_name",
            "last_name": "last_name",
            "email": "new.email@example.com",
            "password": "Pass1234",
        }
        self.content_type = "application/json"

    def test_successful_registration(self) -> None:
        response = self.client.post(self.register_url, data=self.valid_data, content_type=self.content_type)
        logger.debug(f"{response=}")
        user: User | None = User.objects.filter(email=self.valid_data["email"]).first()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["code"], SUCCESS)

        self.assertIsNotNone(user)
        self.assertEqual(user.email, self.valid_data["email"])  # type: ignore

    def test_missing_fields(self) -> None:
        fields = list(self.valid_data)
        for field in fields:
            with self.subTest(missing_filed=field):
                valid_data_copy = self.valid_data
                valid_data_copy.pop(field)
                response = self.client.post(self.register_url, data=valid_data_copy, content_type=self.content_type)
                app_code, http_code = RegistrationErrorResponseFactory.error_codes[MissingRequiredFieldException]
                logger.info(f"Expecting app_code: {app_code} and http_code: {http_code}")

                self.assertEqual(response.status_code, http_code)
                self.assertEqual(response.json()["code"], app_code)

    def test_weak_password(self) -> None:
        for password in ["short", "a" * 100, "WithoutNumbers", "WITHOUT_LOWERCASE_1234", "without_uppercase_1234"]:
            with self.subTest(password=password):
                valid_data_copy = self.valid_data
                valid_data_copy["password"] = password
                response = self.client.post(self.register_url, data=valid_data_copy, content_type=self.content_type)
                app_code, http_code = RegistrationErrorResponseFactory.error_codes[PasswordValidationException]
                logger.info(f"Expecting app_code: {app_code} and http_code: {http_code}")

                self.assertEqual(response.status_code, http_code)
                self.assertEqual(response.json()["code"], app_code)

    def test_invalid_email(self) -> None:
        self.valid_data["email"] = "invalid_email"
        response = self.client.post(self.register_url, data=self.valid_data, content_type=self.content_type)
        app_code, http_code = RegistrationErrorResponseFactory.error_codes[InvalidEmailException]
        logger.info(f"Expecting app_code: {app_code} and http_code: {http_code}")

        self.assertEqual(response.status_code, http_code)
        self.assertEqual(response.json()["code"], app_code)

    def test_too_long_first_name(self) -> None:
        self.valid_data["first_name"] = "A" * 256
        response = self.client.post(self.register_url, data=self.valid_data, content_type=self.content_type)
        app_code, http_code = RegistrationErrorResponseFactory.error_codes[FirstNameIsTooLongException]
        logger.info(f"Expecting app_code: {app_code} and http_code: {http_code}")

        self.assertEqual(response.status_code, http_code)
        self.assertEqual(response.json()["code"], app_code)

    def test_too_long_last_name(self) -> None:
        self.valid_data["last_name"] = "A" * 256
        response = self.client.post(self.register_url, data=self.valid_data, content_type=self.content_type)
        app_code, http_code = RegistrationErrorResponseFactory.error_codes[LastNameIsTooLongException]
        logger.info(f"Expecting app_code: {app_code} and http_code: {http_code}")

        self.assertEqual(response.status_code, http_code)
        self.assertEqual(response.json()["code"], app_code)

    def test_empty_name(self) -> None:
        for name in ["first_name", "last_name"]:
            with self.subTest(empty=name):
                self.valid_data[name] = ""
                response = self.client.post(self.register_url, data=self.valid_data, content_type=self.content_type)
                app_code, http_code = RegistrationErrorResponseFactory.error_codes[EmptyStringException]
                logger.info(f"Expecting app_code: {app_code} and http_code: {http_code}")

                self.assertEqual(response.status_code, http_code)
                self.assertEqual(response.json()["code"], app_code)

    def test_duplicate_email(self) -> None:
        self.client.post(self.register_url, data=self.valid_data, content_type=self.content_type)
        response = self.client.post(self.register_url, data=self.valid_data, content_type=self.content_type)
        app_code, http_code = RegistrationErrorResponseFactory.error_codes[EmailAlreadyExistsException]
        logger.info(f"Expecting app_code: {app_code} and http_code: {http_code}")

        self.assertEqual(response.status_code, http_code)
        self.assertEqual(response.json()["code"], app_code)

    def test_invalid_data_types(self) -> None:
        invalid_type_cases = [
            # (field_name, invalid_value)
            ("first_name", 123),
            ("first_name", True),
            ("last_name", 123.45),
            ("last_name", ["array"]),
            ("last_name", {"key": "value"}),
            ("email", 12345),
            ("email", False),
            ("password", 999999),
            ("password", ["p", "a", "s", "s"]),
        ]

        for field, invalid_value in invalid_type_cases:
            with self.subTest(field=field, invalid_value=invalid_value):
                invalid_data = self.valid_data.copy()
                invalid_data[field] = invalid_value  # type: ignore

                response = self.client.post(self.register_url, data=invalid_data, content_type=self.content_type)

                app_code, http_code = RegistrationErrorResponseFactory.error_codes[ValidationError]
                logger.info(f"Expecting app_code: {app_code} and http_code: {http_code}")
                logger.debug(f"detail: {response.json()["detail"]}")
                self.assertEqual(response.status_code, http_code)
                self.assertEqual(response.json()["code"], app_code)
