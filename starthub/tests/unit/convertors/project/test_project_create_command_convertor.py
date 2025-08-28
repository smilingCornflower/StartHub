import json
from pathlib import Path
from unittest.mock import MagicMock

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import SimpleTestCase
from django.utils.datastructures import MultiValueDict
from domain.value_objects.common import DeadlineDate, Description, FirstName, Id, LastName, PhoneNumber, SocialLink
from domain.value_objects.company import (
    BusinessNumber,
    CompanyFounderCreateCommand,
    CompanyName,
    EstablishedDate,
    PatentNumber,
)
from domain.value_objects.file import FileVo
from domain.value_objects.geo import AddressCreateCommand, CityId, RegionId
from domain.value_objects.project.accelerator import AcceleratorName, ProjectAcceleratorCreateCommand
from domain.value_objects.project.bank_loan import (
    BankLoanOrganizationName,
    LoanAmount,
    LoanTerms,
    ProjectBankLoanCreateCommand,
)
from domain.value_objects.project.bootstrap import ProjectBootstrapCreateCommand
from domain.value_objects.project.common import GoalSum, ProjectName
from domain.value_objects.project.crowdfunding import (
    ProjectCrowdfundingAmount,
    ProjectCrowdfundingCreateCommand,
    ProjectCrowdfundingName,
)
from domain.value_objects.project.funding_model import FundingModelId
from domain.value_objects.project.government_grant import (
    ProjectGovernmentGrantAmount,
    ProjectGovernmentGrantCreateCommand,
    ProjectGrantName,
    ProjectGrantOrganizationName,
)
from domain.value_objects.project.incubator import IncubatorCreateCommand, IncubatorName
from domain.value_objects.project.investment import (
    ProjectInvestmentAmount,
    ProjectInvestmentCreateCommand,
    ProjectInvestmentOrganizationName,
)
from domain.value_objects.project.media import MediaFile
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
from domain.value_objects.project.project import ProjectCreateCommand
from domain.value_objects.project.stage import ProjectStageId
from domain.value_objects.project.step import ProjectStepCreateCommand, ProjectStepDate, ProjectStepName
from domain.value_objects.project.team_member import TeamMemberCreateCommand
from domain.value_objects.project.useful_link import UsefulLinkCreateCommand, UsefulLinkName
from presentation.request_converters.common import parse_date
from presentation.request_converters.project.project_create_command import request_to_project_create_command
from tests.common.constants import KZ_CODE, TEST_FILES_PATH
from tests.common.python_obj_to_mock_request import python_obj_to_mock_request


class TestRequestToProjectCreateCommandIntegration(SimpleTestCase):
    def setUp(self):
        self.test_files_dir = Path(__file__).parent / "test_files"

    def load_real_file(self, filename, content_type):
        file_path = TEST_FILES_PATH / filename
        with open(file_path, "rb") as f:
            return SimpleUploadedFile(filename, f.read(), content_type=content_type)

    def test_minimal_conversion(self):
        project_data = {
            "name": "Test Project",
            "description": "Test description",
            "goal_sum": 1000000,
            "deadline": "2077-12-31",
            "category_ids": [1, 2],
            "funding_model_id": 1,
            "stage_id": 1,
            "social_links": {"instagram": "https://instagram.com/test"},
            "phone_number": "+77123456789",
            "project_steps": [],
        }

        company_data = {
            "name": "Test Company",
            "country_code": "KZ",
            "business_id": "123456789012",
            "established_date": "2020-01-01",
            "address": {
                "country_code": "KZ",
                "region_id": 1,
                "city_id": 1,
                "street": "Test Street",
                "house_number": "123",
            },
        }

        team_members = [{"first_name": "John", "last_name": "Doe", "description": "Lead Developer"}]

        company_founder = {"first_name": "Jane", "last_name": "Smith", "description": "CEO and Founder"}

        request = python_obj_to_mock_request(
            {
                "project": project_data,
                "company": company_data,
                "team_members": team_members,
                "company_founder": company_founder,
            },
            {
                "files": [self.load_real_file("file.pdf", "application/pdf")],
                "media": [self.load_real_file("img.jpg", "image/jpeg")],
            },
        )

        expected_result = ProjectCreateCommand(
            name=ProjectName(value="Test Project"),
            description=Description(value="Test description"),
            goal_sum=GoalSum(value=1000000),
            deadline=DeadlineDate(value=parse_date("2077-12-31")),
            category_ids=[Id(value=1), Id(value=2)],
            creator_id=Id(value=1),
            funding_model_id=FundingModelId(value=1),
            stage_id=ProjectStageId(value=1),
            social_links=[SocialLink(platform="instagram", link="https://instagram.com/test")],
            phone_number=PhoneNumber(value="+77123456789"),
            steps=[],
            files=[FileVo(value=self.load_real_file("file.pdf", "application/pdf").read())],
            media=[MediaFile(value=self.load_real_file("img.jpg", "image/jpeg").read())],
            company_name=CompanyName(value="Test Company"),
            country_code=KZ_CODE,
            company_address=AddressCreateCommand(
                country_code=KZ_CODE,
                region_id=RegionId(value=1),
                city_id=CityId(value=1),
                street="Test Street",
                house_number="123",
                district=None,
                postal_code=None,
                raw_address=None,
            ),
            business_id=BusinessNumber(value="123456789012", country_code=KZ_CODE),
            established_date=EstablishedDate(value=parse_date("2020-01-01")),
            patent_number=None,
            team_members=[
                TeamMemberCreateCommand(
                    first_name=FirstName(value="John"),
                    last_name=LastName(value="Doe"),
                    description=Description(value="Lead Developer"),
                )
            ],
            company_founder=CompanyFounderCreateCommand(
                name=FirstName(value="Jane"),
                surname=LastName(value="Smith"),
                description=Description(value="CEO and Founder"),
            ),
            goal_description=None,
            incubator=None,
            accelerator=None,
            crowdunding=None,
            investment=None,
            government_grant=None,
            bootstrap=None,
            bank_loan=None,
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
            useful_links=None,
        )

        result = request_to_project_create_command(request, user_id=1)

        self.assertEqual(result, expected_result)

    def test_conversion_with_optional_fields(self):
        project_data = {
            "name": "Advanced Project",
            "description": "Advanced description",
            "goal_description": "Goal description",
            "goal_sum": 5000000,
            "deadline": "2077-12-31",
            "category_ids": [1],
            "funding_model_id": 1,
            "stage_id": 2,
            "social_links": {"instagram": "https://instagram.com/advanced", "twitter": "https://twitter.com/advanced"},
            "phone_number": "+77123456789",
            "project_steps": [
                {"name": "Planning Phase", "description": "Initial planning", "date": "2025-11-15"},
                {"name": "Development Phase", "description": "Core development", "date": "2025-12-15"},
            ],
            "ltv": 1000.5,
            "arpu": 50.25,
            "arppu": 75.30,
            "cac": 100.0,
            "nps": 8.5,
            "roi": 15.5,
            "aov": 120.0,
            "churn_rate": 5.2,
            "retention_rate": 85.7,
            "conversion_rate": 3.4,
        }

        company_data = {
            "name": "Advanced Company",
            "country_code": "KZ",
            "business_id": "123456789012",
            "established_date": "2018-06-15",
            "patent_number": "KZ12345",
            "address": {
                "country_code": "KZ",
                "region_id": 2,
                "city_id": 5,
                "district": "Business District",
                "street": "Advanced Street",
                "house_number": "123A",
                "postal_code": "050000",
                "raw_address": "Advanced Street 123A, Business District, Almaty, Kazakhstan",
            },
        }

        team_members = [
            {"first_name": "Alice", "last_name": "Johnson", "description": "CTO"},
            {"first_name": "Bob", "last_name": "Brown", "description": "Lead Designer"},
        ]

        company_founder = {"first_name": "Charlie", "last_name": "Wilson", "description": "Founder and CEO"}

        incubator_data = {"name": "Tech Incubator", "description": "Leading tech incubator"}

        accelerator_data = {"name": "Growth Accelerator", "description": "Business growth accelerator"}

        crowdfunding_data = {"name": "Kickstarter Campaign", "amount": 100000.0}

        investment_data = {
            "organization_name": "Venture Capital Fund",
            "amount": 500000.0,
            "social_links": {"linkedin": "https://linkedin.com/vc"},
            "phone_numbers": ["+77123456780", "+77123456781"],
        }

        government_grant_data = {
            "grant_name": "Innovation Grant",
            "amount": 200000.0,
            "organization_name": "Ministry of Innovation",
        }

        bootstrap_data = {"description": "Self-funded startup"}

        bank_loan_data = {
            "organization_name": "Development Bank",
            "amount": 300000.0,
            "terms": "5 years at 8% interest",
        }

        useful_links = [
            {"name": "Company Website", "url": "https://company.com"},
            {"name": "Product Demo", "url": "https://demo.company.com"},
        ]

        request = python_obj_to_mock_request(
            {
                "project": project_data,
                "company": company_data,
                "team_members": team_members,
                "company_founder": company_founder,
                "incubator": incubator_data,
                "accelerator": accelerator_data,
                "crowdfunding": crowdfunding_data,
                "investment": investment_data,
                "government_grant": government_grant_data,
                "bootstrap": bootstrap_data,
                "bank_loan": bank_loan_data,
                "useful_links": useful_links,
            }
        )

        expected_result = ProjectCreateCommand(
            name=ProjectName(value="Advanced Project"),
            goal_description=Description(value="Goal description"),
            description=Description(value="Advanced description"),
            goal_sum=GoalSum(value=5000000),
            deadline=DeadlineDate(value=parse_date("2077-12-31")),
            category_ids=[Id(value=1)],
            creator_id=Id(value=2),
            funding_model_id=FundingModelId(value=1),
            stage_id=ProjectStageId(value=2),
            social_links=[
                SocialLink(platform="instagram", link="https://instagram.com/advanced"),
                SocialLink(platform="twitter", link="https://twitter.com/advanced"),
            ],
            phone_number=PhoneNumber(value="+77123456789"),
            steps=[
                ProjectStepCreateCommand(
                    name=ProjectStepName(value="Planning Phase"),
                    description=Description(value="Initial planning"),
                    date=ProjectStepDate(value=parse_date("2025-11-15")),
                ),
                ProjectStepCreateCommand(
                    name=ProjectStepName(value="Development Phase"),
                    description=Description(value="Core development"),
                    date=ProjectStepDate(value=parse_date("2025-12-15")),
                ),
            ],
            files=[],
            media=[],
            company_name=CompanyName(value="Advanced Company"),
            country_code=KZ_CODE,
            company_address=AddressCreateCommand(
                country_code=KZ_CODE,
                region_id=RegionId(value=2),
                city_id=CityId(value=5),
                district="Business District",
                street="Advanced Street",
                house_number="123A",
                postal_code="050000",
                raw_address="Advanced Street 123A, Business District, Almaty, Kazakhstan",
            ),
            business_id=BusinessNumber(value="123456789012", country_code=KZ_CODE),
            established_date=EstablishedDate(value=parse_date("2018-06-15")),
            patent_number=PatentNumber(value="KZ12345"),
            team_members=[
                TeamMemberCreateCommand(
                    first_name=FirstName(value="Alice"),
                    last_name=LastName(value="Johnson"),
                    description=Description(value="CTO"),
                ),
                TeamMemberCreateCommand(
                    first_name=FirstName(value="Bob"),
                    last_name=LastName(value="Brown"),
                    description=Description(value="Lead Designer"),
                ),
            ],
            company_founder=CompanyFounderCreateCommand(
                name=FirstName(value="Charlie"),
                surname=LastName(value="Wilson"),
                description=Description(value="Founder and CEO"),
            ),
            incubator=IncubatorCreateCommand(
                name=IncubatorName(value="Tech Incubator"), description=Description(value="Leading tech incubator")
            ),
            accelerator=ProjectAcceleratorCreateCommand(
                name=AcceleratorName(value="Growth Accelerator"),
                description=Description(value="Business growth accelerator"),
            ),
            crowdunding=ProjectCrowdfundingCreateCommand(
                name=ProjectCrowdfundingName(value="Kickstarter Campaign"),
                amount=ProjectCrowdfundingAmount(value=100000.0),
            ),
            investment=ProjectInvestmentCreateCommand(
                organization_name=ProjectInvestmentOrganizationName(value="Venture Capital Fund"),
                amount=ProjectInvestmentAmount(value=500000.0),
                social_links=[SocialLink(platform="linkedin", link="https://linkedin.com/vc")],
                phone_numbers=[PhoneNumber(value="+77123456780"), PhoneNumber(value="+77123456781")],
            ),
            government_grant=ProjectGovernmentGrantCreateCommand(
                grant_name=ProjectGrantName(value="Innovation Grant"),
                amount=ProjectGovernmentGrantAmount(value=200000.0),
                organization_name=ProjectGrantOrganizationName(value="Ministry of Innovation"),
            ),
            bootstrap=ProjectBootstrapCreateCommand(description=Description(value="Self-funded startup")),
            bank_loan=ProjectBankLoanCreateCommand(
                organization_name=BankLoanOrganizationName(value="Development Bank"),
                amount=LoanAmount(value=300000.0),
                terms=LoanTerms(value="5 years at 8% interest"),
            ),
            useful_links=[
                UsefulLinkCreateCommand(name=UsefulLinkName(value="Company Website"), url="https://company.com"),
                UsefulLinkCreateCommand(name=UsefulLinkName(value="Product Demo"), url="https://demo.company.com"),
            ],
            ltv=Ltv(value=1000.5),
            arpu=Arpu(value=50.25),
            arppu=Arppu(value=75.30),
            cac=Cac(value=100.0),
            nps=Nps(value=8.5),
            roi=Roi(value=15.5),
            aov=Aov(value=120.0),
            churn_rate=ChurnRate(value=5.2),
            retention_rate=RetentionRate(value=85.7),
            conversion_rate=ConversionRate(value=3.4),
        )

        result = request_to_project_create_command(request, user_id=2)

        self.assertEqual(result, expected_result)
