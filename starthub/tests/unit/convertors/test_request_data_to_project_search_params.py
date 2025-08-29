from dataclasses import dataclass
from unittest.mock import Mock

from django.http import QueryDict
from django.test import SimpleTestCase
from domain.value_objects.project.common import ProjectName
from domain.value_objects.search import ProjectSearchParams
from presentation.request_converters.search import request_data_to_project_search_params


@dataclass
class ValidProjectSearchData:
    name = "My Project"
    name_field = "name"


class TestRequestDataToProjectSearchParams(SimpleTestCase):
    def setUp(self):
        self.data = ValidProjectSearchData()

    def apply_function(self, query_string):
        query = QueryDict(query_string)
        return request_data_to_project_search_params(query)

    def test_no_query_params(self):
        expected = ProjectSearchParams(name=None)

        result = self.apply_function("")
        self.assertEqual(expected, result)

    def test_with_name(self):
        expected = ProjectSearchParams(name=ProjectName(value=self.data.name))

        result = self.apply_function(f"{self.data.name_field}={self.data.name}")
        self.assertEqual(expected, result)
