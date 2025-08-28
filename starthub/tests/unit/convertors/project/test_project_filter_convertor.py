from dataclasses import dataclass
from unittest.mock import Mock

from django.http import QueryDict
from django.test import SimpleTestCase
from domain.value_objects.common import Id, Slug
from domain.value_objects.filter import ProjectFilter
from domain.value_objects.project.common import ProjectStageVo, ProjectStatus
from presentation.request_converters.project.project_filter import request_to_project_filter


@dataclass
class ValidProjectFilterData:
    category_slug = "test-category"
    funding_model_slug = "test-funding"
    status = ["active", "under_moderation"]
    stage = "mvp"
    user_id = 123

    category_slug_field = "category_slug"
    funding_model_slug_field = "funding_model_slug"
    status_field = "status"
    stage_field = "stage"
    user_id_field = "user_id"


class TestRequestToProjectFilter(SimpleTestCase):
    def setUp(self):
        self.valid_dataclass = ValidProjectFilterData()

    def test_valid_data_with_all_fields(self):
        request = Mock()
        query_params = QueryDict(mutable=True)
        query_params[self.valid_dataclass.category_slug_field] = self.valid_dataclass.category_slug
        query_params[self.valid_dataclass.funding_model_slug_field] = self.valid_dataclass.funding_model_slug
        query_params.setlist(self.valid_dataclass.status_field, self.valid_dataclass.status)
        query_params[self.valid_dataclass.stage_field] = self.valid_dataclass.stage
        query_params[self.valid_dataclass.user_id_field] = str(self.valid_dataclass.user_id)
        request.query_params = query_params

        expected = ProjectFilter(
            category_slug=Slug(value=self.valid_dataclass.category_slug),
            funding_model_slug=Slug(value=self.valid_dataclass.funding_model_slug),
            statuses=[ProjectStatus(value=status) for status in self.valid_dataclass.status],
            stage=ProjectStageVo(value=self.valid_dataclass.stage),
            user_id=Id(value=self.valid_dataclass.user_id),
        )
        result = request_to_project_filter(request)
        self.assertEqual(expected, result)

    def test_valid_data_with_category_slug_only(self):
        request = Mock()
        query_params = QueryDict(mutable=True)
        query_params[self.valid_dataclass.category_slug_field] = self.valid_dataclass.category_slug
        request.query_params = query_params

        expected = ProjectFilter(category_slug=Slug(value=self.valid_dataclass.category_slug))
        result = request_to_project_filter(request)
        self.assertEqual(expected, result)

    def test_valid_data_with_funding_model_slug_only(self):
        request = Mock()
        query_params = QueryDict(mutable=True)
        query_params[self.valid_dataclass.funding_model_slug_field] = self.valid_dataclass.funding_model_slug
        request.query_params = query_params

        expected = ProjectFilter(funding_model_slug=Slug(value=self.valid_dataclass.funding_model_slug))
        result = request_to_project_filter(request)
        self.assertEqual(expected, result)

    def test_valid_data_with_status_only(self):
        request = Mock()
        query_params = QueryDict(mutable=True)
        query_params.setlist(self.valid_dataclass.status_field, self.valid_dataclass.status)
        request.query_params = query_params

        expected = ProjectFilter(statuses=[ProjectStatus(value=status) for status in self.valid_dataclass.status])
        result = request_to_project_filter(request)
        self.assertEqual(expected, result)

    def test_valid_data_with_stage_only(self):
        request = Mock()
        query_params = QueryDict(mutable=True)
        query_params[self.valid_dataclass.stage_field] = self.valid_dataclass.stage
        request.query_params = query_params

        expected = ProjectFilter(stage=ProjectStageVo(value=self.valid_dataclass.stage))
        result = request_to_project_filter(request)
        self.assertEqual(expected, result)

    def test_valid_data_with_user_id_only(self):
        request = Mock()
        query_params = QueryDict(mutable=True)
        query_params[self.valid_dataclass.user_id_field] = str(self.valid_dataclass.user_id)
        request.query_params = query_params

        expected = ProjectFilter(user_id=Id(value=self.valid_dataclass.user_id))
        result = request_to_project_filter(request)
        self.assertEqual(expected, result)

    def test_empty_query_params(self):
        request = Mock()
        query_params = QueryDict()
        request.query_params = query_params

        expected = ProjectFilter()

        result = request_to_project_filter(request)
        self.assertEqual(expected, result)
