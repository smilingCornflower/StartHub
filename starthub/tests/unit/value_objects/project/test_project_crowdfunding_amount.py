from django.test import SimpleTestCase
from domain.constants import PROJECT_CROWDFUNDING_AMOUNT_MAX_DIGITS
from domain.exceptions.project_management import ProjectCrowdfundingMaxAmountException
from domain.value_objects.project.crowdfunding import ProjectCrowdfundingAmount


class TestData:
    VALID_AMOUNT = 1000.0
    TOO_BIG_AMOUNT = 10**PROJECT_CROWDFUNDING_AMOUNT_MAX_DIGITS


class ProjectCrowdfundingAmountTests(SimpleTestCase):
    def test_valid_amount(self):
        obj = ProjectCrowdfundingAmount(value=TestData.VALID_AMOUNT)
        self.assertEqual(obj.value, TestData.VALID_AMOUNT)

    def test_too_big_amount_raises_exception(self):
        with self.assertRaises(ProjectCrowdfundingMaxAmountException):
            ProjectCrowdfundingAmount(value=TestData.TOO_BIG_AMOUNT)

    def test_almost_max_amount_is_ok(self):
        almost_max = TestData.TOO_BIG_AMOUNT - 1
        obj = ProjectCrowdfundingAmount(value=almost_max)
        self.assertEqual(obj.value, almost_max)
