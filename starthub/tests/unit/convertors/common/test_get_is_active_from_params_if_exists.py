from dataclasses import dataclass
from unittest.mock import Mock

from django.http import QueryDict
from django.test import SimpleTestCase
from domain.exceptions.validation import ValidationException
from presentation.request_converters.user_management.user import get_is_active_if_exists_from_params


@dataclass
class ValidIsActiveData:
    is_active_true = "true"
    is_active_false = "false"
    invalid_is_active = "invalid_value"

    is_active_field = "is_active"


class TestGetIsActiveIfExistsFromParams(SimpleTestCase):
    def setUp(self):
        self.valid_dataclass = ValidIsActiveData()

    def test_is_active_true(self):
        params = QueryDict(mutable=True)
        params[self.valid_dataclass.is_active_field] = self.valid_dataclass.is_active_true

        expected = True

        result = get_is_active_if_exists_from_params(params)
        self.assertEqual(expected, result)

    def test_is_active_false(self):
        params = QueryDict(mutable=True)
        params[self.valid_dataclass.is_active_field] = self.valid_dataclass.is_active_false

        expected = False

        result = get_is_active_if_exists_from_params(params)
        self.assertEqual(expected, result)

    def test_no_is_active_parameter(self):
        params = QueryDict()

        expected = None

        result = get_is_active_if_exists_from_params(params)
        self.assertEqual(expected, result)

    def test_invalid_is_active_value(self):
        params = QueryDict(mutable=True)
        params[self.valid_dataclass.is_active_field] = self.valid_dataclass.invalid_is_active

        with self.assertRaises(ValidationException):
            get_is_active_if_exists_from_params(params)
