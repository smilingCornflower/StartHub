import pydantic
from django.test import SimpleTestCase
from domain.exceptions.company import CompanyNameIsTooLongException
from domain.exceptions.project_management import ProjectNameIsTooLongException
from domain.exceptions.validation import EmptyStringException
from domain.value_objects.company import CompanyName
from domain.value_objects.project_management import ProjectName


class TestProjectAndCompanyName(SimpleTestCase):
    def check_raises(self, exc, func):
        self.assertTrue(f":raises {exc.__name__}:" in func.__doc__, "raises not in docstring.")

    def test_valid_name(self):
        project_name = ProjectName(value="Project Name")
        company_name = CompanyName(value="Company Name")
        self.assertEqual(project_name.value, "Project Name")
        self.assertEqual(company_name.value, "Company Name")

    def test_empty_name(self):
        with self.assertRaises(EmptyStringException):
            ProjectName(value="")
        with self.assertRaises(EmptyStringException):
            CompanyName(value="")

        self.check_raises(EmptyStringException, ProjectName.is_valid_name)
        self.check_raises(EmptyStringException, CompanyName.is_valid_name)

    def test_too_large_name(self):
        with self.assertRaises(ProjectNameIsTooLongException):
            ProjectName(value="a" * 256)
        with self.assertRaises(CompanyNameIsTooLongException):
            CompanyName(value="a" * 256)

        self.check_raises(ProjectNameIsTooLongException, ProjectName.is_valid_name)
        self.check_raises(CompanyNameIsTooLongException, CompanyName.is_valid_name)

    def test_incorrect_type(self):
        with self.assertRaises(pydantic.ValidationError):
            ProjectName(value=10)
        with self.assertRaises(pydantic.ValidationError):
            CompanyName(value=10)
