from django.test import SimpleTestCase
from domain.exceptions.validation import StringIsTooLongException
from domain.value_objects.common import Description


class TestDescription(SimpleTestCase):
    def check_raises(self, exc, func):
        self.assertTrue(f":raises {exc.__name__}:" in func.__doc__, "raises not in docstring.")

    def test_valid_description(self):
        description = Description(value="description")
        self.assertEqual(description.value, "description")

    def test_too_long_description(self):
        with self.assertRaises(StringIsTooLongException):
            Description(value="A" * 2001)

        self.check_raises(StringIsTooLongException, Description.validate_description_length)
