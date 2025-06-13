from datetime import date, timedelta

from django.test import SimpleTestCase
from domain.exceptions.validation import DeadlineInPastException
from domain.value_objects.common import DeadlineDate


class TestDeadlineDate(SimpleTestCase):
    def check_raises(self, exc, func):
        self.assertTrue(f":raises {exc.__name__}:" in func.__doc__, "raises not in docstring.")

    def test_valid_deadline(self):
        valid_date = date.today() + timedelta(days=1)
        deadline = DeadlineDate(value=valid_date)
        self.assertEqual(deadline.value, valid_date)

    def test_date_in_past(self):
        incorrect_date = date(2020, 1, 1)
        with self.assertRaises(DeadlineInPastException):
            DeadlineDate(value=incorrect_date)
        self.check_raises(DeadlineInPastException, DeadlineDate.validate_deadline_not_in_past)
