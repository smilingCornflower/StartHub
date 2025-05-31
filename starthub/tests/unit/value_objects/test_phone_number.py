from django.test import TestCase
from domain.exceptions.validation import InvalidPhoneNumberException
from domain.value_objects.common import PhoneNumber
from pydantic import ValidationError


class PhoneNumberTestCase(TestCase):
    def test_valid_phone_numbers(self) -> None:
        """Checks correct format numbers in E164."""
        test_cases: list[tuple[str, str]] = [
            ("+79123456789", "+79123456789"),
            ("+380441234567", "+380441234567"),
            ("+12125551234", "+12125551234"),
            ("+442071838750", "+442071838750"),
            ("+7912 345 67 89", "+79123456789"),
            ("+7(912)345-67-89", "+79123456789"),
        ]
        for input_phone, expected_phone in test_cases:
            phone = PhoneNumber(value=input_phone)
            self.assertEqual(phone.value, expected_phone)

    def test_invalid_phone_numbers(self) -> None:
        invalid_phones = [
            "123",  # too short
            "+1 234 567 89012",  # too long
            "+999123456789",  # invalid country code
            "1234567890"  # missing country code
            "abcdefghijk",  # non-numeric
            "+1@#$%^&*()",  # garbage characters
            "+7 123 456 78 90",  # incorrect Russian format
            "",
        ]

        for invalid_phone in invalid_phones:
            with self.subTest(invalid_phone=invalid_phone):
                with self.assertRaises(InvalidPhoneNumberException):
                    PhoneNumber(value=invalid_phone)

        with self.subTest(invalid_phone=None):
            with self.assertRaises(ValidationError):
                PhoneNumber(value=None)  # type: ignore
