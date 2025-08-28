from dataclasses import dataclass
from datetime import date

from django.test import SimpleTestCase
from domain.exceptions.validation import DateIsNotIsoFormatException
from presentation.request_converters.common import parse_date


@dataclass
class DateData:
    valid_date = "2023-12-25"
    invalid_date = "25/12/2023"
    invalid_format = "not-a-date"


class TestParseDate(SimpleTestCase):
    def setUp(self):
        self.data = DateData()

    def test_valid_iso_date(self):
        expected = date.fromisoformat(self.data.valid_date)

        result = parse_date(self.data.valid_date)
        self.assertEqual(expected, result)

    def test_invalid_date_format(self):
        with self.assertRaises(DateIsNotIsoFormatException):
            parse_date(self.data.invalid_date)

    def test_invalid_string(self):
        with self.assertRaises(DateIsNotIsoFormatException):
            parse_date(self.data.invalid_format)
