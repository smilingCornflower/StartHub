from dataclasses import dataclass
from unittest.mock import Mock

from django.test import SimpleTestCase
from domain.value_objects.common import Description
from domain.value_objects.project.stage import ProjectStageUpdateCommand
from presentation.request_converters.project.stage import request_to_project_stage_update_command


@dataclass
class ValidProjectStageData:
    description = "Test Stage Description"

    description_field = "description"

    def to_dict(self):
        return {
            self.description_field: self.description,
        }


class TestRequestToProjectStageUpdateCommand(SimpleTestCase):
    def setUp(self):
        self.valid_dataclass = ValidProjectStageData()

    def test_valid_data_with_description(self):
        request = Mock()
        request.data = self.valid_dataclass.to_dict()

        expected = ProjectStageUpdateCommand(description=Description(value=self.valid_dataclass.description))
        result = request_to_project_stage_update_command(request)
        self.assertEqual(expected, result)

    def test_empty_data(self):
        request = Mock()
        request.data = {}

        expected = ProjectStageUpdateCommand(description=None)
        result = request_to_project_stage_update_command(request)
        self.assertEqual(expected, result)
