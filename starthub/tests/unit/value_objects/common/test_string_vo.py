from django.test import SimpleTestCase
from domain.exceptions.validation import EmptyStringException, StringIsTooLongException
from domain.value_objects.common import StringVo
from tests.common.check_raises import check_raises_in_docs


class TestStringVo(SimpleTestCase):
    def test_valid_string(self):
        valid_string = "Valid String"
        string = StringVo(value=valid_string)
        self.assertEqual(string.value, valid_string)

    def test_empty_string_exception(self):
        exception = EmptyStringException
        with self.assertRaises(exception):
            StringVo(value="")
        check_raises_in_docs(StringVo.validate_string, exception)

    def test_custom_max_length(self):
        class CustomString(StringVo):
            max_length = 10

        exception = StringIsTooLongException
        with self.assertRaises(exception):
            CustomString(value="Too long string.")
        check_raises_in_docs(CustomString.validate_string, exception)

    def test_custom_empty_string_exception(self):
        class CustomException(Exception):
            pass

        class CustomString(StringVo):
            empty_string_exception = CustomException

        with self.assertRaises(CustomException):
            CustomString(value="")

    def test_custom_too_long_string_exception(self):
        class CustomException(Exception):
            pass

        class CustomString(StringVo):
            max_length = 10
            too_long_string_exception = CustomException

        with self.assertRaises(CustomException):
            CustomString(value="Too long string.")

    def test_get_default_too_long_string_msg(self):
        msg = StringVo.get_too_long_string_msg()
        self.assertEqual(msg, "String is too long.")
