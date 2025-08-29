from dataclasses import dataclass
from unittest.mock import Mock

from django.http import QueryDict
from django.test import SimpleTestCase
from domain.value_objects.common import FirstName, LastName
from domain.value_objects.user_management.user import Email, UserGetCommand
from presentation.request_converters.user_management.user import request_to_user_get_command
from rest_framework.request import Request


@dataclass
class ValidUserGetData:
    email = "john.doe@example.com"
    first_name = "John"
    last_name = "Doe"
    date_joined_start = "2024-01-01"
    date_joined_end = "2024-12-31"
    role = "admin"
    is_active = "true"

    email_field = "email"
    first_name_field = "first_name"
    last_name_field = "last_name"
    date_joined_start_field = "date_joined_start"
    date_joined_end_field = "date_joined_end"
    role_field = "role"
    is_active_field = "is_active"


class TestRequestToUserGetCommand(SimpleTestCase):
    def setUp(self):
        self.data = ValidUserGetData()

    def apply_function(self, query_string):
        request = Mock(spec=Request)
        request.query_params = QueryDict(query_string)
        return request_to_user_get_command(request)

    def test_no_query_params(self):
        expected = UserGetCommand(
            role=None,
            is_active=None,
            email=None,
            first_name=None,
            last_name=None,
            date_joined_start=None,
            date_joined_end=None,
        )

        result = self.apply_function("")
        self.assertEqual(expected, result)

    def test_with_email_only(self):
        expected = UserGetCommand(
            role=None,
            is_active=None,
            email=Email(value=self.data.email),
            first_name=None,
            last_name=None,
            date_joined_start=None,
            date_joined_end=None,
        )

        result = self.apply_function(f"{self.data.email_field}={self.data.email}")
        self.assertEqual(expected, result)

    def test_with_first_name_only(self):
        expected = UserGetCommand(
            role=None,
            is_active=None,
            email=None,
            first_name=FirstName(value=self.data.first_name),
            last_name=None,
            date_joined_start=None,
            date_joined_end=None,
        )

        result = self.apply_function(f"{self.data.first_name_field}={self.data.first_name}")
        self.assertEqual(expected, result)

    def test_with_last_name_only(self):
        expected = UserGetCommand(
            role=None,
            is_active=None,
            email=None,
            first_name=None,
            last_name=LastName(value=self.data.last_name),
            date_joined_start=None,
            date_joined_end=None,
        )

        result = self.apply_function(f"{self.data.last_name_field}={self.data.last_name}")
        self.assertEqual(expected, result)

    def test_with_date_joined_start_only(self):
        from datetime import date

        expected = UserGetCommand(
            role=None,
            is_active=None,
            email=None,
            first_name=None,
            last_name=None,
            date_joined_start=date(2024, 1, 1),
            date_joined_end=None,
        )

        result = self.apply_function(f"{self.data.date_joined_start_field}={self.data.date_joined_start}")
        self.assertEqual(expected, result)

    def test_with_date_joined_end_only(self):
        from datetime import date

        expected = UserGetCommand(
            role=None,
            is_active=None,
            email=None,
            first_name=None,
            last_name=None,
            date_joined_start=None,
            date_joined_end=date(2024, 12, 31),
        )

        result = self.apply_function(f"{self.data.date_joined_end_field}={self.data.date_joined_end}")
        self.assertEqual(expected, result)

    def test_with_all_fields(self):
        from datetime import date

        from domain.enums.role import RoleEnum

        expected = UserGetCommand(
            role=RoleEnum(value="admin"),
            is_active=True,
            email=Email(value=self.data.email),
            first_name=FirstName(value=self.data.first_name),
            last_name=LastName(value=self.data.last_name),
            date_joined_start=date(2024, 1, 1),
            date_joined_end=date(2024, 12, 31),
        )

        query_string = (
            f"{self.data.email_field}={self.data.email}&"
            f"{self.data.first_name_field}={self.data.first_name}&"
            f"{self.data.last_name_field}={self.data.last_name}&"
            f"{self.data.date_joined_start_field}={self.data.date_joined_start}&"
            f"{self.data.date_joined_end_field}={self.data.date_joined_end}&"
            f"{self.data.role_field}={self.data.role}&"
            f"{self.data.is_active_field}={self.data.is_active}"
        )

        result = self.apply_function(query_string)
        self.assertEqual(expected, result)
