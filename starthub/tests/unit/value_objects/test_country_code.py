from django.test import SimpleTestCase
from domain.exceptions.geo.country import InvalidCountryCodeException
from domain.value_objects.geo import CountryCode


class TestCountryCode(SimpleTestCase):
    def test_valid_country_code(self):
        code = CountryCode(value="US")

        self.assertEqual(code.value, "US")

    def test_too_long_code(self):
        with self.assertRaises(InvalidCountryCodeException):
            CountryCode(value="USA")  # length > 2

    def test_not_alpha_code(self):
        with self.assertRaises(InvalidCountryCodeException):
            CountryCode(value="U1")  # contains a digit

    def test_not_uppercase_code(self):
        with self.assertRaises(InvalidCountryCodeException):
            CountryCode(value="us")  # contains a lowecase symbol

    def test_invalid_country_code_nonexistent(self):
        with self.assertRaises(InvalidCountryCodeException):
            CountryCode(value="ZZ")  # right format, but there is not such country
