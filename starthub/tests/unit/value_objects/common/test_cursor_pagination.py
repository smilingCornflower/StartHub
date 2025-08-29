from dataclasses import dataclass

from django.test import SimpleTestCase
from domain.constants import PAGINNATION_MAX_LMIT
from domain.exceptions.pagination import PaginationMaxLimitException
from domain.value_objects.common import CursorPagination


@dataclass
class CursorPaginationTestData:
    valid_limit = 10
    max_limit = PAGINNATION_MAX_LMIT
    invalid_limit = PAGINNATION_MAX_LMIT + 1
    valid_last_id = 123


class TestCursorPagination(SimpleTestCase):
    def setUp(self):
        self.data = CursorPaginationTestData()

    def test_valid_pagination_without_last_id(self):
        pagination = CursorPagination(limit=self.data.valid_limit)

        self.assertEqual(pagination.limit, self.data.valid_limit)
        self.assertIsNone(pagination.last_id)

    def test_valid_pagination_with_last_id(self):
        pagination = CursorPagination(limit=self.data.valid_limit, last_id=self.data.valid_last_id)

        self.assertEqual(pagination.limit, self.data.valid_limit)
        self.assertEqual(pagination.last_id, self.data.valid_last_id)

    def test_limit_at_max_value(self):
        pagination = CursorPagination(limit=self.data.max_limit)

        self.assertEqual(pagination.limit, self.data.max_limit)

    def test_limit_exceeds_max_value(self):
        with self.assertRaises(PaginationMaxLimitException) as context:
            CursorPagination(limit=self.data.invalid_limit)

        self.assertIn(str(self.data.max_limit), str(context.exception))
