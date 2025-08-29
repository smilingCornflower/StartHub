from dataclasses import dataclass
from datetime import date, timedelta

from django.test import SimpleTestCase
from domain.exceptions.validation import DateInFutureException
from domain.value_objects.company import EstablishedDate
from tests.utils import check_raises


@dataclass
class EstablishedDateTestData:
    _today = None
    _past_date = None
    _future_date = None

    @property
    def today(self):
        if self._today is None:
            self._today = date.today()
        return self._today

    @property
    def past_date(self):
        if self._past_date is None:
            self._past_date = date.today() - timedelta(days=365)
        return self._past_date

    @property
    def future_date(self):
        if self._future_date is None:
            self._future_date = date.today() + timedelta(days=1)
        return self._future_date


class TestEstablishedDate(SimpleTestCase):
    def setUp(self):
        self.data = EstablishedDateTestData()

    def test_valid_today_date(self):
        established = EstablishedDate(value=self.data.today)

        self.assertEqual(established.value, self.data.today)

    def test_valid_past_date(self):
        established = EstablishedDate(value=self.data.past_date)

        self.assertEqual(established.value, self.data.past_date)

    def test_future_date_raises(self):
        exc = DateInFutureException

        check_raises(EstablishedDate.validate_date_not_in_future, exc)
        with self.assertRaises(exc):
            EstablishedDate(value=self.data.future_date)
