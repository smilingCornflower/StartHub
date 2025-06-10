from django.test import SimpleTestCase
from domain.value_objects.country import CountryCode
from pydantic import ValidationError


class CountryCodeValidationTest(SimpleTestCase):
    def test_valid_country_codes(self) -> None:
        valid_codes = ["US", "GB", "DE", "FR", "RU", "JP", "CN"]

        for code in valid_codes:
            with self.subTest(code=code):
                country_code = CountryCode(value=code)
                self.assertEqual(country_code.value, code)

    def test_invalid_country_codes(self) -> None:
        invalid_cases = [
            "usa",  # lowercase
            "Us",  # mixed case
            "U",  # too short
            "USA",  # too long
            "U1",  # digit
            "U-S",  # hyphen
            "",
            "  ",
            None,
        ]

        for code in invalid_cases:
            with self.subTest(code=code):
                with self.assertRaises(ValidationError):
                    CountryCode(value=code)  # type: ignore
