from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import SimpleTestCase
from domain.value_objects.common import DeadlineDate, Description, Id
from domain.value_objects.file import PdfFile
from domain.value_objects.project.common import GoalSum, ProjectName
from domain.value_objects.project.funding_model import FundingModelId
from domain.value_objects.project.incubator import IncubatorName, IncubatorUpdatePayload
from domain.value_objects.project.metric import (
    Aov,
    Arppu,
    Arpu,
    Cac,
    ChurnRate,
    ConversionRate,
    Ltv,
    Nps,
    RetentionRate,
    Roi,
)
from domain.value_objects.project.project import ProjectUpdateCommand
from domain.value_objects.project.stage import ProjectStageId
from domain.value_objects.project.step import ProjectStepCreateCommand, ProjectStepDate, ProjectStepName
from presentation.request_converters.common import parse_date
from presentation.request_converters.project.project_update_command import request_to_the_project_update_command
from tests.common.constants import TEST_FILES_PATH
from tests.common.python_obj_to_mock_request import python_obj_to_mock_request


class TestRequestToProjectUpdateCommand(SimpleTestCase):
    def load_real_file(self, filename, content_type):
        file_path = TEST_FILES_PATH / filename
        with open(file_path, "rb") as f:
            return SimpleUploadedFile(filename, f.read(), content_type=content_type)

    def test_empty_update_conversion(self):
        request = python_obj_to_mock_request(dict())
        expected_result = ProjectUpdateCommand(
            project_id=Id(value=123),
            user_id=Id(value=456),
            name=None,
            description=None,
            goal_description=None,
            category_ids=None,
            funding_model_id=None,
            stage_id=None,
            steps=None,
            goal_sum=None,
            deadline=None,
            plan_file=None,
            incubator=None,
            ltv=None,
            arpu=None,
            arppu=None,
            cac=None,
            nps=None,
            roi=None,
            aov=None,
            churn_rate=None,
            retention_rate=None,
            conversion_rate=None,
        )

        result = request_to_the_project_update_command(request, project_id=123, user_id=456)

        self.assertEqual(result, expected_result)

    def test_full_update_conversion(self):
        project_data = {
            "name": "Fully Updated Project",
            "description": "Updated description",
            "goal_description": "Updated goal description",
            "category_ids": [1, 2, 3],
            "funding_model_id": 2,
            "stage_id": 3,
            "goal_sum": 2000000,
            "deadline": "2026-01-15",
            "project_steps": [
                {"name": "Updated Planning", "description": "Updated planning phase", "date": "2077-03-01"},
                {"name": "Updated Development", "description": "Updated development phase", "date": "2077-07-15"},
            ],
            "incubator": {"name": "Updated Incubator", "description": "Updated incubator description"},
            "ltv": 1500.75,
            "arpu": 75.50,
            "arppu": 100.25,
            "cac": 150.0,
            "nps": 9.2,
            "roi": 20.5,
            "aov": 180.0,
            "churn_rate": 3.8,
            "retention_rate": 92.5,
            "conversion_rate": 4.2,
        }

        request = python_obj_to_mock_request(
            {"project": project_data}, {"project_plan": self.load_real_file("file.pdf", "application/pdf")}
        )

        expected_result = ProjectUpdateCommand(
            project_id=Id(value=789),
            user_id=Id(value=101),
            name=ProjectName(value="Fully Updated Project"),
            description=Description(value="Updated description"),
            goal_description=Description(value="Updated goal description"),
            category_ids=[Id(value=1), Id(value=2), Id(value=3)],
            funding_model_id=FundingModelId(value=2),
            stage_id=ProjectStageId(value=3),
            goal_sum=GoalSum(value=2000000),
            deadline=DeadlineDate(value=parse_date("2026-01-15")),
            steps=[
                ProjectStepCreateCommand(
                    name=ProjectStepName(value="Updated Planning"),
                    description=Description(value="Updated planning phase"),
                    date=ProjectStepDate(value=parse_date("2077-03-01")),
                ),
                ProjectStepCreateCommand(
                    name=ProjectStepName(value="Updated Development"),
                    description=Description(value="Updated development phase"),
                    date=ProjectStepDate(value=parse_date("2077-07-15")),
                ),
            ],
            plan_file=PdfFile(value=self.load_real_file("file.pdf", "application/pdf").read()),
            incubator=IncubatorUpdatePayload(
                project_id=Id(value=789),
                name=IncubatorName(value="Updated Incubator"),
                description=Description(value="Updated incubator description"),
            ),
            ltv=Ltv(value=1500.75),
            arpu=Arpu(value=75.50),
            arppu=Arppu(value=100.25),
            cac=Cac(value=150.0),
            nps=Nps(value=9.2),
            roi=Roi(value=20.5),
            aov=Aov(value=180.0),
            churn_rate=ChurnRate(value=3.8),
            retention_rate=RetentionRate(value=92.5),
            conversion_rate=ConversionRate(value=4.2),
        )

        result = request_to_the_project_update_command(request, project_id=789, user_id=101)

        self.assertEqual(result, expected_result)
