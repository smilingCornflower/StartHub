from django.test import SimpleTestCase
from domain.exceptions.project_management import InvalidProjectStatusException
from domain.value_objects.project.common import ProjectStatus
from tests.utils import check_raises


class TestData:
    VALID_STATUS = "active"
    INVALID_STATUS = "not_a_status"


class TestProjectStatus(SimpleTestCase):
    def test_valid_status(self):
        obj = ProjectStatus(value=TestData.VALID_STATUS)
        self.assertEqual(obj.value, TestData.VALID_STATUS)

    def test_invalid_status_raises_exception(self):
        exc = InvalidProjectStatusException
        check_raises(ProjectStatus.is_valid_stage, exc)
        with self.assertRaises(exc):
            ProjectStatus(value=TestData.INVALID_STATUS)

    def test_case_insensitive_status(self):
        obj = ProjectStatus(value=TestData.VALID_STATUS.upper())
        self.assertEqual(obj.value, TestData.VALID_STATUS)
