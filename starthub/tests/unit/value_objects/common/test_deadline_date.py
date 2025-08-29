from datetime import date, timedelta

from django.test import SimpleTestCase
from domain.exceptions.validation import DeadlineInPastException
from domain.value_objects.common import DeadlineDate
from tests.common.check_raises import check_raises_in_docs


class TestDeadlineDate(SimpleTestCase):
    def test_valid_deadline(self):
        deadline_date = date.today() + timedelta(days=1)
        deadline = DeadlineDate(value=deadline_date)
        self.assertEqual(deadline.value, deadline_date)

    def test_deadline_in_past_exc(self):
        exception = DeadlineInPastException
        with self.assertRaises(exception):
            d = date.today() - timedelta(days=1)
            DeadlineDate(value=d)
        check_raises_in_docs(DeadlineDate.validate_deadline_not_in_past, exception)
