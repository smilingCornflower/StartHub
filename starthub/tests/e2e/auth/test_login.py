import jwt
from django.test import TestCase
from django.urls import reverse
from loguru import logger
from pydantic import ValidationError
from rest_framework.test import APIClient

from domain.constants import JWT_ALGORITHM
from domain.enums.token import TokenTypeEnum
from domain.exceptions.auth import InvalidCredentialsException, PasswordValidationException
from domain.exceptions.user import UserNotFoundException
from domain.exceptions.validation import InvalidEmailException, EmptyStringException
from domain.models.user import User
from presentation.constants import SUCCESS
from presentation.response_factories.common import LoginErrorResponseFactory


class TestLogin(TestCase):
    user: User
    client: APIClient
    login_url: str
    content_type: str

    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = User.objects.create_user(
            first_name="first_name",
            last_name="last_name",
            email="email@example.com",
            password="Pass1234",
        )
        cls.login_url = reverse("login")
        cls.client = APIClient()
        cls.content_type = "application/json"

    def setUp(self) -> None:
        self.valid_credentials = {
            "email": "email@example.com",
            "password": "Pass1234"
        }

    def test_successful_login(self) -> None:
        response = self.client.post(self.login_url, data=self.valid_credentials, content_type=self.content_type)

        access: str = response.cookies.get("access_token").value  # type: ignore
        refresh: str = response.cookies.get("refresh_token").value  # type: ignore

        logger.debug(f"access = {access}")
        logger.debug(f"refresh = {refresh}")

        access_decoded = jwt.decode(access, algorithms=JWT_ALGORITHM, options={"verify_signature": False})
        refresh_decoded = jwt.decode(refresh, algorithms=JWT_ALGORITHM, options={"verify_signature": False})

        self.assertEqual(int(access_decoded["sub"]), self.user.id)
        self.assertEqual(access_decoded["email"], self.user.email)
        self.assertEqual(access_decoded["type"], TokenTypeEnum.ACCESS)

        self.assertEqual(int(refresh_decoded["sub"]), self.user.id)
        self.assertEqual(refresh_decoded["type"], TokenTypeEnum.REFRESH)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], SUCCESS)

    def test_another_email(self) -> None:
        self.valid_credentials["email"] = 'another-email@example.com'
        response = self.client.post(self.login_url, data=self.valid_credentials, content_type=self.content_type)
        app_code, http_code = LoginErrorResponseFactory.error_codes[UserNotFoundException]
        logger.info(f"Expecting app_code: {app_code} and http_code: {http_code}")

        self.assertEqual(response.status_code, http_code)
        self.assertEqual(response.json()["code"], app_code)

    def test_invalid_email(self) -> None:
        self.valid_credentials["email"] = 'invalid-email?!@example'

        response = self.client.post(self.login_url, data=self.valid_credentials, content_type=self.content_type)
        app_code, http_code = LoginErrorResponseFactory.error_codes[InvalidEmailException]
        logger.info(f"Expecting app_code: {app_code} and http_code: {http_code}")

        self.assertEqual(response.status_code, http_code)
        self.assertEqual(response.json()["code"], app_code)

    def test_incorrect_password(self) -> None:
        self.valid_credentials["password"] = 'NotCorrectPass1234'
        response = self.client.post(self.login_url, data=self.valid_credentials, content_type=self.content_type)
        app_code, http_code = LoginErrorResponseFactory.error_codes[InvalidCredentialsException]
        logger.info(f"Expecting app_code: {app_code} and http_code: {http_code}")

        self.assertEqual(response.status_code, http_code)
        self.assertEqual(response.json()["code"], app_code)

    def test_weak_password(self) -> None:
        self.valid_credentials["password"] = 'weak_pass'
        response = self.client.post(self.login_url, data=self.valid_credentials, content_type=self.content_type)
        app_code, http_code = LoginErrorResponseFactory.error_codes[PasswordValidationException]
        logger.info(f"Expecting app_code: {app_code} and http_code: {http_code}")

        self.assertEqual(response.status_code, http_code)
        self.assertEqual(response.json()["code"], app_code)

    def test_login_with_nonexistent_email_returns_user_not_found_error(self) -> None:
        """
        Tests that attempting to log in with a non-existent email returns a UserNotFound error, regardless of the provided password.
        """
        response = self.client.post(
            self.login_url, data={"email": 'another.email@example.com', "password": 'invalid-pass'},
            content_type=self.content_type)
        app_code, http_code = LoginErrorResponseFactory.error_codes[UserNotFoundException]
        logger.info(f"Expecting app_code: {app_code} and http_code: {http_code}")
        self.assertEqual(response.status_code, http_code)
        self.assertEqual(response.json()["code"], app_code)


    def test_missing_fields(self) -> None:
        for field in list(self.valid_credentials):
            with self.subTest(missing_field=field):
                valid_data_copy = self.valid_credentials.copy()
                valid_data_copy.pop(field)
                response = self.client.post(self.login_url, data=valid_data_copy, content_type=self.content_type)
                app_code, http_code = LoginErrorResponseFactory.error_codes[KeyError]
                logger.info(f"Expecting app_code: {app_code} and http_code: {http_code}")
                self.assertEqual(response.status_code, http_code)
                self.assertEqual(response.json()["code"], app_code)

    def test_empty_fields(self) -> None:
        for field in list(self.valid_credentials):
            with self.subTest(missing_field=field):
                valid_data_copy = self.valid_credentials.copy()
                valid_data_copy[field] = ""

                response = self.client.post(self.login_url, data=valid_data_copy, content_type=self.content_type)
                app_code, http_code = LoginErrorResponseFactory.error_codes[EmptyStringException]

                logger.info(f"Expecting app_code: {app_code} and http_code: {http_code}")
                self.assertEqual(response.status_code, http_code)
                self.assertEqual(response.json()["code"], app_code)

    def test_incorrect_data_types(self) -> None:
        invalid_data_types = [
            {"email": 123, "password": "Pass1234"},
            {"email": True, "password": "Pass1234"},
            {"email": ["email@example.com"], "password": "Pass1234"},
            {"email": {"email": "email@example.com"}, "password": "Pass1234"},
            {"email": "email@example.com", "password": 12345678},
            {"email": "email@example.com", "password": True},
            {"email": "email@example.com", "password": ["Pass1234"]},
            {"email": "email@example.com", "password": {"password": "Pass1234"}},
        ]

        for invalid_data in invalid_data_types:
            with self.subTest(invalid_data=invalid_data):
                response = self.client.post(
                    self.login_url,
                    data=invalid_data,
                    content_type=self.content_type
                )
                app_code, http_code = LoginErrorResponseFactory.error_codes[ValidationError]
                logger.info(f"Expecting app_code: {app_code} and http_code: {http_code}")

                self.assertEqual(response.status_code, http_code)
                self.assertEqual(response.json()["code"], app_code)