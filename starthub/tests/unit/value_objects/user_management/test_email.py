from django.test import SimpleTestCase
from domain.exceptions.validation import EmptyStringException, InvalidEmailException
from domain.value_objects.user_management.user import Email
from tests.common.check_raises import check_raises


class TestEmail(SimpleTestCase):
    def test_valid_email(self):
        val = "test@example.com"
        email = Email(value=val)
        assert email.value == val

    def test_empty_email(self):
        exc = EmptyStringException
        with self.assertRaises(exc):
            Email(value="")
        check_raises(Email.validate_email, exc)

    def test_invalid_email(self):
        exc = InvalidEmailException
        with self.assertRaises(exc):
            Email(value="invalid-email")
        check_raises(Email.validate_email, exc)
