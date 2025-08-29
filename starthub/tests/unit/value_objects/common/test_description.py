from django.test import SimpleTestCase
from domain.constants import DESCRIPTION_MAX_LENGTH
from domain.exceptions.validation import EmptyStringException, StringIsTooLongException
from domain.value_objects.common import Description


class TestDescription(SimpleTestCase):
    def test_valid_descr(self):
        val = "description"
        desc = Description(value=val)
        self.assertEqual(desc.value, val)

    def test_too_long_string(self):
        with self.assertRaises(StringIsTooLongException):
            val = "a" * DESCRIPTION_MAX_LENGTH + "a"
            Description(value=val)

    def test_empty_string(self):
        with self.assertRaises(EmptyStringException):
            Description(value="")
