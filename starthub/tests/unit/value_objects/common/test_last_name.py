from django.test import SimpleTestCase
from domain.constants import CHAR_FIELD_SHORT_LENGTH
from domain.exceptions.validation import EmptyStringException, FirstNameIsTooLongException, LastNameIsTooLongException
from domain.value_objects.common import LastName


class TestLastName(SimpleTestCase):
    def test_valid_name(self):
        val = "Surname"
        last_name = LastName(value=val)
        self.assertEqual(last_name.value, val)

    def test_empty_name(self):
        with self.assertRaises(EmptyStringException):
            LastName(value="")

    def test_too_long_name(self):
        val = "a" * CHAR_FIELD_SHORT_LENGTH + "a"
        with self.assertRaises(LastNameIsTooLongException):
            LastName(value=val)
