from django.test import SimpleTestCase
from domain.exceptions.auth import PasswordValidationException
from domain.exceptions.validation import EmptyStringException
from domain.value_objects.user_management.user import RawPassword
from tests.common.check_raises import check_raises_in_docs


class TestRawPassword(SimpleTestCase):
    def test_valid_password(self):
        val = "ValidPass1234"
        password = RawPassword(value=val)
        assert password.value == val

    def test_empty_password(self):
        exc = EmptyStringException
        with self.assertRaises(exc):
            RawPassword(value="")
        check_raises_in_docs(RawPassword.validate_password, exc)

    def test_docstring_contains_validation_exc(self):
        check_raises_in_docs(RawPassword.validate_password, PasswordValidationException)

    def test_too_short_password(self):
        with self.assertRaises(PasswordValidationException):
            RawPassword(value="A1b")

    def test_too_long_password(self):
        with self.assertRaises(PasswordValidationException):
            RawPassword(value="A" * 129 + "1b")

    def test_no_uppercase(self):
        with self.assertRaises(PasswordValidationException):
            RawPassword(value="password123")

    def test_no_lowercase(self):
        with self.assertRaises(PasswordValidationException):
            RawPassword(value="PASSWORD123")

    def test_no_digit(self):
        with self.assertRaises(PasswordValidationException):
            RawPassword(value="Password")
