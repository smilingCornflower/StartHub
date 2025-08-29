from django.test import SimpleTestCase
from domain.constants import PROJECT_INVESTMENTS_PHONE_MAX_AMOUNT
from domain.enums.social_links import SocialPlatformEnum
from domain.exceptions.project_management import ProjectInvestmentPhoneMaxAmountException
from domain.value_objects.common import PhoneNumber, SocialLink
from domain.value_objects.project.investment import (
    ProjectInvestmentAmount,
    ProjectInvestmentCreateCommand,
    ProjectInvestmentOrganizationName,
)
from tests.utils import check_raises


class TestData:
    org = ProjectInvestmentOrganizationName(value="Org")
    amount = ProjectInvestmentAmount(value=1000)
    social_links = [SocialLink(platform=SocialPlatformEnum.INSTAGRAM, link="https://instagram.com/example_profile")]

    @staticmethod
    def get_phones(n: int) -> list[PhoneNumber]:
        return [PhoneNumber(value=f"+7700100000{i}") for i in range(n)]


class ProjectInvestmentCreateCommandTest(SimpleTestCase):
    def test_valid_data(self):
        ProjectInvestmentCreateCommand(
            organization_name=TestData.org,
            amount=TestData.amount,
            social_links=TestData.social_links,
            phone_numbers=TestData.get_phones(1),
        )

    def test_too_many_phone_numbers(self):
        exc = ProjectInvestmentPhoneMaxAmountException
        check_raises(ProjectInvestmentCreateCommand.check_max_amount, exc)
        with self.assertRaises(exc):
            ProjectInvestmentCreateCommand(
                organization_name=TestData.org,
                amount=TestData.amount,
                social_links=TestData.social_links,
                phone_numbers=TestData.get_phones(PROJECT_INVESTMENTS_PHONE_MAX_AMOUNT),
            )
