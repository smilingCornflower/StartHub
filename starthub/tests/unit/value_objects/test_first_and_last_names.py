from django.test import SimpleTestCase
from domain.constants import CHAR_FIELD_SHORT_LENGTH
from domain.exceptions.validation import EmptyStringException, FirstNameIsTooLongException, LastNameIsTooLongException
from domain.value_objects.common import FirstName, LastName
from pydantic import ValidationError


class NameValidationTests(SimpleTestCase):
    def test_first_name_validation(self) -> None:
        FirstName(value="Valid Name")
        FirstName(value="A")
        FirstName(value="A" * CHAR_FIELD_SHORT_LENGTH)

        with self.assertRaises(EmptyStringException):
            FirstName(value="")

        with self.assertRaises(EmptyStringException):
            FirstName(value=" " * 10)

        with self.assertRaises(FirstNameIsTooLongException):
            FirstName(value="A" * (CHAR_FIELD_SHORT_LENGTH + 1))

        with self.assertRaises(ValidationError):
            FirstName(value=None)  # type: ignore

    def test_last_name_validation(self) -> None:
        LastName(value="Valid Lastname")
        LastName(value="B")
        LastName(value="B" * CHAR_FIELD_SHORT_LENGTH)

        with self.assertRaises(EmptyStringException):
            LastName(value="")

        with self.assertRaises(EmptyStringException):
            LastName(value=" " * 10)

        with self.assertRaises(LastNameIsTooLongException):
            LastName(value="B" * (CHAR_FIELD_SHORT_LENGTH + 1))

        with self.assertRaises(ValidationError):
            LastName(value=None)  # type: ignore
