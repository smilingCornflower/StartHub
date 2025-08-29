from django.test import SimpleTestCase
from domain.exceptions.validation import InvalidPhoneNumberException
from domain.value_objects.common import PhoneNumber
from tests.common.check_raises import check_raises_in_docs


class TestPhoneNumber(SimpleTestCase):
    def test_valid_number(self):
        valid_number = "+77001234567"
        number = PhoneNumber(value=valid_number)
        self.assertEqual(number.value, valid_number)

    def test_invalid_number(self):
        exception = InvalidPhoneNumberException
        with self.assertRaises(exception):
            PhoneNumber(value="invalid")

        with self.assertRaises(exception):
            PhoneNumber(value="+71234567890")  # 123 - not a valid operator code for +7 (Russia/Kazakhstan)

        check_raises_in_docs(PhoneNumber.validate_phone_number, exception)
