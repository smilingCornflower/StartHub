from dataclasses import dataclass

from django.test import SimpleTestCase
from domain.exceptions.company import CompanyNameIsTooLongException
from domain.exceptions.validation import EmptyStringException
from domain.value_objects.common import CHAR_FIELD_MAX_LENGTH
from domain.value_objects.company import CompanyName


@dataclass
class CompanyNameTestData:
    _valid_name = None
    _empty_name = None
    _too_long_name = None

    @property
    def valid_name(self):
        if self._valid_name is None:
            self._valid_name = "OpenAI"
        return self._valid_name

    @property
    def empty_name(self):
        if self._empty_name is None:
            self._empty_name = ""
        return self._empty_name

    @property
    def too_long_name(self):
        if self._too_long_name is None:
            self._too_long_name = "A" * (CHAR_FIELD_MAX_LENGTH + 1)
        return self._too_long_name


class TestCompanyName(SimpleTestCase):
    def setUp(self):
        self.data = CompanyNameTestData()

    def test_valid_name(self):
        company = CompanyName(value=self.data.valid_name)

        self.assertEqual(company.value, self.data.valid_name)

    def test_empty_name(self):
        exc = EmptyStringException

        with self.assertRaises(exc):
            CompanyName(value=self.data.empty_name)

    def test_too_long_name(self):
        exc = CompanyNameIsTooLongException

        with self.assertRaises(exc):
            CompanyName(value=self.data.too_long_name)
