from dataclasses import dataclass
from unittest.mock import Mock

from django.http import QueryDict
from django.test import SimpleTestCase
from domain.exceptions.validation import MissingRequiredFieldException
from domain.value_objects.common import CursorPagination, OffsetPagination
from presentation.request_converters.common import request_to_cursor_pagination, request_to_offset_pagination


@dataclass
class ValidCursorPaginationData:
    last_id = 100
    limit = 20

    last_id_field = "last_id"
    limit_field = "limit"


@dataclass
class ValidOffsetPaginationData:
    page_number = 2
    limit = 25

    page_number_field = "page_number"
    limit_field = "limit"


class TestRequestToCursorPagination(SimpleTestCase):
    def setUp(self):
        self.valid_dataclass = ValidCursorPaginationData()

    def test_valid_data_with_last_id(self):
        request = Mock()
        query_params = QueryDict(mutable=True)
        query_params[self.valid_dataclass.last_id_field] = str(self.valid_dataclass.last_id)
        query_params[self.valid_dataclass.limit_field] = str(self.valid_dataclass.limit)
        request.query_params = query_params

        expected = CursorPagination(last_id=self.valid_dataclass.last_id, limit=self.valid_dataclass.limit)

        result = request_to_cursor_pagination(request)
        self.assertEqual(expected, result)

    def test_valid_data_without_last_id(self):
        request = Mock()
        query_params = QueryDict(mutable=True)
        query_params[self.valid_dataclass.limit_field] = str(self.valid_dataclass.limit)
        request.query_params = query_params

        expected = CursorPagination(last_id=None, limit=self.valid_dataclass.limit)

        result = request_to_cursor_pagination(request)
        self.assertEqual(expected, result)

    def test_missing_limit(self):
        request = Mock()
        query_params = QueryDict(mutable=True)
        query_params[self.valid_dataclass.last_id_field] = str(self.valid_dataclass.last_id)
        request.query_params = query_params

        with self.assertRaises(MissingRequiredFieldException):
            request_to_cursor_pagination(request)


class TestRequestToOffsetPagination(SimpleTestCase):
    def setUp(self):
        self.valid_dataclass = ValidOffsetPaginationData()

    def test_valid_data_with_page_number(self):
        request = Mock()
        query_params = QueryDict(mutable=True)
        query_params[self.valid_dataclass.page_number_field] = str(self.valid_dataclass.page_number)
        query_params[self.valid_dataclass.limit_field] = str(self.valid_dataclass.limit)
        request.query_params = query_params

        expected_offset = (self.valid_dataclass.page_number - 1) * self.valid_dataclass.limit
        expected = OffsetPagination(offset=expected_offset, limit=self.valid_dataclass.limit)

        result = request_to_offset_pagination(request)
        self.assertEqual(expected, result)

    def test_valid_data_without_page_number(self):
        request = Mock()
        query_params = QueryDict(mutable=True)
        query_params[self.valid_dataclass.limit_field] = str(self.valid_dataclass.limit)
        request.query_params = query_params

        expected = OffsetPagination(offset=0, limit=self.valid_dataclass.limit)

        result = request_to_offset_pagination(request)
        self.assertEqual(expected, result)

    def test_missing_limit(self):
        request = Mock()
        query_params = QueryDict(mutable=True)
        query_params[self.valid_dataclass.page_number_field] = str(self.valid_dataclass.page_number)
        request.query_params = query_params

        with self.assertRaises(MissingRequiredFieldException):
            request_to_offset_pagination(request)
