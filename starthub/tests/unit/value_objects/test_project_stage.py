from django.test import SimpleTestCase
from loguru import logger

from domain.enums.project_stage import ProjectStageEnum
from domain.exceptions.project_management import InvalidProjectStageException
from domain.value_objects.project_management import ProjectStage

class TestProjectStage(SimpleTestCase):
    def test_allowed_values(self) -> None:
        allowed_values: list[str] = list(ProjectStageEnum)

        for stage in allowed_values:
            project_stage = ProjectStage(value=stage)
            self.assertEqual(project_stage.value, stage)

    def test_invalid_value(self) -> None:
        with self.assertRaises(InvalidProjectStageException):
            ProjectStage(value="not-a-stage")

    def test_uppercase(self) -> None:
        project_stage = ProjectStage(value="IDEA")
        self.assertEqual(project_stage.value, "idea")