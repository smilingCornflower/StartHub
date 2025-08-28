from dataclasses import dataclass
from unittest.mock import Mock

from django.http import QueryDict
from django.test import SimpleTestCase
from domain.enums.role import RoleEnum
from domain.exceptions.validation import ValidationException
from presentation.request_converters.common import get_role_if_exists_from_params


@dataclass
class ValidRoleData:
    role = "admin"
    invalid_role = "invalid_role"

    role_field = "role"


class TestGetRoleIfExistsFromParams(SimpleTestCase):
    def setUp(self):
        self.valid_dataclass = ValidRoleData()

    def test_valid_role(self):
        params = QueryDict(mutable=True)
        params[self.valid_dataclass.role_field] = self.valid_dataclass.role

        expected = RoleEnum(value=self.valid_dataclass.role)

        result = get_role_if_exists_from_params(params)
        self.assertEqual(expected, result)

    def test_no_role_parameter(self):
        params = QueryDict()

        expected = None

        result = get_role_if_exists_from_params(params)
        self.assertEqual(expected, result)

    def test_invalid_role_value(self):
        params = QueryDict(mutable=True)
        params[self.valid_dataclass.role_field] = self.valid_dataclass.invalid_role

        with self.assertRaises(ValidationException):
            get_role_if_exists_from_params(params)
