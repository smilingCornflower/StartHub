from django.test import SimpleTestCase
from domain.exceptions.validation import NegativeNumberException
from domain.value_objects.common import PositiveNumber
from tests.common.check_raises import check_raises_in_docs


class TestPositiveNumber(SimpleTestCase):
    def test_positive_number(self):
        val = 3.14
        number = PositiveNumber(value=val)
        self.assertEqual(number.value, val)

    def test_negative_number(self):
        with self.assertRaises(NegativeNumberException):
            PositiveNumber(value=-10)
        check_raises_in_docs(PositiveNumber.validate_positive_number, NegativeNumberException)
