from django.test import SimpleTestCase
from domain.enums.project_stage import ProjectStageEnum
from domain.exceptions.project_management import InvalidProjectStageException
from domain.value_objects.project.common import ProjectStageVo


class TestProjectStage(SimpleTestCase):
    def test_allowed_values(self) -> None:
        allowed_values: list[str] = list(ProjectStageEnum)

        for stage in allowed_values:
            project_stage = ProjectStageVo(value=stage)
            self.assertEqual(project_stage.value, stage)

    def test_invalid_value(self) -> None:
        with self.assertRaises(InvalidProjectStageException):
            ProjectStageVo(value="not-a-stage")

    def test_uppercase(self) -> None:
        project_stage = ProjectStageVo(value="IDEA")
        self.assertEqual(project_stage.value, "idea")
