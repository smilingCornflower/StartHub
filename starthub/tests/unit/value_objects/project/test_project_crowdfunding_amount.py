from django.test import SimpleTestCase
from domain.constants import PROJECT_CROWDFUNDING_AMOUNT_MAX_DIGITS
from domain.exceptions.project_management import ProjectCrowdfundingMaxAmountException
from domain.value_objects.project.crowdfunding import ProjectCrowdfundingAmount
from tests.utils import check_raises


class TestData:
    VALID_AMOUNT = 1000.0
    TOO_BIG_AMOUNT = 10**PROJECT_CROWDFUNDING_AMOUNT_MAX_DIGITS


class TestProjectCrowdfundingAmount(SimpleTestCase):
    def test_valid_amount(self):
        obj = ProjectCrowdfundingAmount(value=TestData.VALID_AMOUNT)
        self.assertEqual(obj.value, TestData.VALID_AMOUNT)

    def test_too_big_amount_raises_exception(self):
        exc = ProjectCrowdfundingMaxAmountException
        check_raises(ProjectCrowdfundingAmount.validate_funding_max_amount, exc)
        with self.assertRaises(exc):
            ProjectCrowdfundingAmount(value=TestData.TOO_BIG_AMOUNT)

    def test_almost_max_amount_is_ok(self):
        almost_max = TestData.TOO_BIG_AMOUNT - 1
        obj = ProjectCrowdfundingAmount(value=almost_max)
        self.assertEqual(obj.value, almost_max)
