from dataclasses import dataclass
from unittest.mock import Mock

from django.test import SimpleTestCase
from domain.exceptions.validation import MissingRequiredFieldException
from domain.value_objects.common import PhoneNumber
from presentation.request_converters.project.common import request_to_phone


@dataclass
class ValidPhoneData:
    phone_number = "+77771234567"

    phone_number_field = "phone_number"

    def to_dict(self):
        return {
            self.phone_number_field: self.phone_number,
        }


class TestRequestToPhone(SimpleTestCase):
    def setUp(self):
        self.valid_dataclass = ValidPhoneData()

    def test_valid_data(self):
        request = Mock()
        request.data = self.valid_dataclass.to_dict()

        expected = PhoneNumber(value=self.valid_dataclass.phone_number)

        result = request_to_phone(request)
        self.assertEqual(expected, result)

    def test_missing_phone_number_field(self):
        request = Mock()
        request.data = {}

        with self.assertRaises(MissingRequiredFieldException):
            request_to_phone(request)
