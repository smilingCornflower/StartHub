from django.test import SimpleTestCase
from domain.constants import CHAR_FIELD_SHORT_LENGTH
from domain.exceptions.validation import EmptyStringException, FirstNameIsTooLongException
from domain.value_objects.common import FirstName
from tests.common.check_raises import check_raises


class TestFirstName(SimpleTestCase):
    def test_valid_name(self):
        val = "Name"
        first_name = FirstName(value=val)
        self.assertEqual(first_name.value, val)

    def test_empty_name(self):
        with self.assertRaises(EmptyStringException):
            FirstName(value="")

    def test_too_long_name(self):
        val = "a" * CHAR_FIELD_SHORT_LENGTH + "a"
        with self.assertRaises(FirstNameIsTooLongException):
            FirstName(value=val)
