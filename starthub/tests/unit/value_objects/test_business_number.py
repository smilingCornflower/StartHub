from unittest.mock import patch

from django.test import TestCase
from domain.exceptions.validation import ValidationException
from domain.validators.business_number import KZBusinessNumberValidator
from domain.value_objects.company import BusinessNumber
from domain.value_objects.country import CountryCode
from pydantic import ValidationError


class BusinessNumberValidationTest(TestCase):
    def test_valid_kz_business_number(self) -> None:
        test_data = {"country_code": CountryCode(value="KZ"), "value": "123456789012"}
        business_number = BusinessNumber(**test_data)  # type: ignore
        self.assertEqual(business_number.country_code.value, "KZ")
        self.assertEqual(business_number.value, "123456789012")

    def test_invalid_kz_business_number(self) -> None:
        with self.assertRaises(ValidationException):
            BusinessNumber(country_code=CountryCode(value="KZ"), value="invalid")

    def test_non_kz_country_accepts_any_value(self) -> None:
        test_data = {"country_code": CountryCode(value="US"), "value": "any-value"}
        business_number = BusinessNumber(**test_data)  # type: ignore
        self.assertEqual(business_number.value, "any-value")

    def test_missing_country_code(self) -> None:
        with self.assertRaises(ValidationError):
            BusinessNumber(value="1234567890")  # type: ignore
