from django.test import SimpleTestCase
from domain.exceptions.validation import ValidationException
from domain.value_objects.company import BusinessNumber
from tests.common.check_raises import check_raises_in_docs
from tests.common.constants import KZ_CODE


class TestBusinessNumber(SimpleTestCase):
    def test_valid_kz_number(self):
        val = "123456789012"
        number = BusinessNumber(country_code=KZ_CODE, value=val)
        assert number.value == val

    def test_invalid_kz_number(self):
        exception = ValidationException
        with self.assertRaises(exception):
            BusinessNumber(country_code=KZ_CODE, value="invalid")
        check_raises_in_docs(BusinessNumber.is_correct_business_number, exception)
