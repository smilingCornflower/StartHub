from django.test import SimpleTestCase
from domain.constants import CHAR_FIELD_MAX_LENGTH
from domain.exceptions.project_management import ProjectNameIsTooLongException
from domain.exceptions.validation import EmptyStringException
from domain.value_objects.project.common import ProjectName
from tests.utils import check_raises


class TestData:
    VALID_NAME = "My Project"
    TOO_LONG_NAME = "x" * (CHAR_FIELD_MAX_LENGTH + 1)


class TestProjectName(SimpleTestCase):
    def test_valid_name(self):
        obj = ProjectName(value=TestData.VALID_NAME)
        self.assertEqual(obj.value, TestData.VALID_NAME)

    def test_empty_name_raises_exception(self):
        with self.assertRaises(EmptyStringException) as cm:
            ProjectName(value="")

    def test_too_long_name_raises_exception(self):
        with self.assertRaises(ProjectNameIsTooLongException) as cm:
            ProjectName(value=TestData.TOO_LONG_NAME)
