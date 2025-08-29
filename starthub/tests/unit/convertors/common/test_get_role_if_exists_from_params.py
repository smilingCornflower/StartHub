from dataclasses import dataclass

from django.http import QueryDict
from django.test import SimpleTestCase
from domain.enums.role import RoleEnum
from domain.exceptions.validation import ValidationException
from presentation.request_converters.common import get_role_if_exists_from_params
from tests.common.check_raises import check_raises


@dataclass
class RoleData:
    role = "admin"
    invalid_role = "invalid_role"

    role_field = "role"


class TestGetRoleIfExistsFromParams(SimpleTestCase):
    def setUp(self):
        self.data = RoleData()

    def test_valid_role(self):
        params = QueryDict(mutable=True)
        params[self.data.role_field] = self.data.role

        expected = RoleEnum(value=self.data.role)

        result = get_role_if_exists_from_params(params)
        self.assertEqual(expected, result)

    def test_no_role_parameter(self):
        params = QueryDict()

        expected = None

        result = get_role_if_exists_from_params(params)
        self.assertEqual(expected, result)

    def test_invalid_role_value(self):
        params = QueryDict(mutable=True)
        params[self.data.role_field] = self.data.invalid_role

        check_raises(get_role_if_exists_from_params, ValidationException)
        with self.assertRaises(ValidationException):
            get_role_if_exists_from_params(params)
