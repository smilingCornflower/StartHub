from dataclasses import dataclass
from unittest.mock import Mock

from django.test import SimpleTestCase
from domain.exceptions.validation import MissingRequiredFieldException
from domain.value_objects.project.report import ProjectReportContent
from domain.value_objects.project.submission import ProjectRejectCommand
from presentation.request_converters.project.submission import request_to_project_submission_reject_command


@dataclass
class ValidProjectSubmissionData:
    report = "Project rejected due to insufficient documentation"

    report_field = "report"

    def to_dict(self):
        return {
            self.report_field: self.report,
        }


class TestRequestToProjectSubmissionRejectCommand(SimpleTestCase):
    def setUp(self):
        self.valid_dataclass = ValidProjectSubmissionData()

    def test_valid_data(self):
        request = Mock()
        request.data = self.valid_dataclass.to_dict()

        expected = ProjectRejectCommand(report=ProjectReportContent(value=self.valid_dataclass.report))

        result = request_to_project_submission_reject_command(request)
        self.assertEqual(expected, result)

    def test_missing_report_field(self):
        request = Mock()
        request.data = {}

        with self.assertRaises(MissingRequiredFieldException):
            request_to_project_submission_reject_command(request)
