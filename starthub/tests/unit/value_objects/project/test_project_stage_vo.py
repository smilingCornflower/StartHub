from django.test import SimpleTestCase
from domain.exceptions.project_management import InvalidProjectStageException
from domain.value_objects.project.common import ProjectStageVo
from tests.utils import check_raises


class TestData:
    VALID_STAGE = "idea"
    INVALID_STAGE = "invalid_stage"


class TestProjectStageVo(SimpleTestCase):
    def test_valid_stage(self):
        obj = ProjectStageVo(value=TestData.VALID_STAGE)
        self.assertEqual(obj.value, TestData.VALID_STAGE)

    def test_invalid_stage_raises_exception(self):
        exc = InvalidProjectStageException
        check_raises(ProjectStageVo.is_valid_stage, exc)
        with self.assertRaises(exc):
            ProjectStageVo(value=TestData.INVALID_STAGE)

    def test_case_insensitive_stage(self):
        obj = ProjectStageVo(value=TestData.VALID_STAGE.upper())
        self.assertEqual(obj.value, TestData.VALID_STAGE)
