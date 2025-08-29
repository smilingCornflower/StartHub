from datetime import date

from application.builders.app_service.project_management.project import ProjectCreateAppServiceBuilder
from django.test import TestCase
from domain.constants import PROJECT_STEPS_MAX_AMOUNT
from domain.exceptions.company import BusinessNumberAlreadyExistsException
from domain.exceptions.geo.city import CityNotFoundException
from domain.exceptions.geo.region import RegionNotFoundException
from domain.exceptions.project_management import (
    FundingModelNotFoundException,
    ProjectCategoryNotFoundException,
    ProjectStageNotFoundException,
    ProjectStepMaxAmountException,
)
from domain.exceptions.user import UserNotFoundException
from domain.models.geo.city import City
from domain.models.geo.country import Country
from domain.models.geo.region import Region
from domain.models.project_management.category import ProjectCategory
from domain.models.project_management.funding_model import FundingModel
from domain.models.project_management.project_stage import ProjectStage
from domain.value_objects.common import DeadlineDate, Description, FirstName, Id, LastName, PhoneNumber, SocialLink
from domain.value_objects.company import BusinessNumber, CompanyFounderCreateCommand, CompanyName, EstablishedDate
from domain.value_objects.country import CountryCode
from domain.value_objects.geo import AddressCreateCommand, CityId, RegionId
from domain.value_objects.project.common import GoalSum, ProjectName
from domain.value_objects.project.funding_model import FundingModelId
from domain.value_objects.project.project import ProjectCreateCommand
from domain.value_objects.project.stage import ProjectStageId
from domain.value_objects.project.step import ProjectStepCreateCommand, ProjectStepDate, ProjectStepName
from domain.value_objects.project.team_member import TeamMemberCreateCommand
from tests.common.builders import get_test_user
from tests.common.check_raises import check_raises_in_docs


class TestProjectCreateAppService(TestCase):
    def get_valid_project_create_command(self):
        return ProjectCreateCommand(
            name=ProjectName(value="Test Project"),
            description=Description(value="Test description"),
            goal_sum=GoalSum(value=1000000),
            deadline=DeadlineDate(value=date(2077, 12, 31)),
            category_ids=[Id(value=self.category_id)],
            creator_id=Id(value=self.user_id),
            funding_model_id=FundingModelId(value=self.funding_model_id),
            stage_id=ProjectStageId(value=self.stage_id),
            social_links=[SocialLink(platform="instagram", link="https://instagram.com/test")],
            phone_number=PhoneNumber(value="+77123456789"),
            steps=[],
            files=[],
            media=[],
            company_name=CompanyName(value="Test Company"),
            country_code=CountryCode(value="KZ"),
            company_address=AddressCreateCommand(
                country_code=CountryCode(value="KZ"),
                region_id=RegionId(value=self.region_id),
                city_id=CityId(value=self.city_id),
                street="Test Street",
                house_number="123",
            ),
            business_id=BusinessNumber(value="123456789012", country_code=CountryCode(value="KZ")),
            established_date=EstablishedDate(value=date(2020, 1, 1)),
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
            incubator=None,
            accelerator=None,
            crowdunding=None,
            investment=None,
            government_grant=None,
            bootstrap=None,
            bank_loan=None,
            patent_number=None,
        )

    def setUp(self):
        self.service = ProjectCreateAppServiceBuilder.create_service()
        self.user = get_test_user()

        self.user_id = self.user.id

        category, _ = ProjectCategory.objects.get_or_create(name="Category")
        funding_model, _ = FundingModel.objects.get_or_create(name="Funding Model")
        stage, _ = ProjectStage.objects.get_or_create(name="Stage")
        country, _ = Country.objects.get_or_create(code="KZ")
        region, _ = Region.objects.get_or_create(name="Region", country=country)
        city, _ = City.objects.get_or_create(name="City", region=region)

        self.category_id = category.id
        self.funding_model_id = funding_model.id
        self.stage_id = stage.id
        self.country_id = country.id
        self.region_id = region.id
        self.city_id = city.id

    def test_create_with_valid_command(self):
        command = self.get_valid_project_create_command()
        self.service.create(command=command, user_id=Id(value=self.user.id))

    def test_with_nonexist_user(self):
        self.user_id = -1
        check_raises_in_docs(self.service.create, UserNotFoundException)
        with self.assertRaises(UserNotFoundException):
            self.service.create(command=self.get_valid_project_create_command(), user_id=Id(value=self.user_id))

    def test_create_with_nonexist_category(self):
        self.category_id = -1
        check_raises_in_docs(self.service.create, ProjectCategoryNotFoundException)
        with self.assertRaises(ProjectCategoryNotFoundException):
            self.service.create(command=self.get_valid_project_create_command(), user_id=Id(value=self.user_id))

    def test_create_with_nonexist_project_stage(self):
        self.stage_id = -1
        check_raises_in_docs(self.service.create, ProjectStageNotFoundException)
        with self.assertRaises(ProjectStageNotFoundException):
            self.service.create(command=self.get_valid_project_create_command(), user_id=Id(value=self.user_id))

    def test_create_with_nonexist_funding_model(self):
        self.funding_model_id = -1
        check_raises_in_docs(self.service.create, FundingModelNotFoundException)
        with self.assertRaises(FundingModelNotFoundException):
            self.service.create(command=self.get_valid_project_create_command(), user_id=Id(value=self.user_id))

    def test_create_with_unavailabll_business_number(self):
        self.service.create(command=self.get_valid_project_create_command(), user_id=Id(value=self.user_id))
        check_raises_in_docs(self.service.create, BusinessNumberAlreadyExistsException)
        with self.assertRaises(BusinessNumberAlreadyExistsException):
            self.service.create(command=self.get_valid_project_create_command(), user_id=Id(value=self.user_id))

    def test_create_with_nonexist_city(self):
        self.city_id = -1
        check_raises_in_docs(self.service.create, CityNotFoundException)
        with self.assertRaises(CityNotFoundException):
            self.service.create(command=self.get_valid_project_create_command(), user_id=Id(value=self.user_id))

    def test_create_with_nonexist_region(self):
        self.region_id = -1
        check_raises_in_docs(self.service.create, RegionNotFoundException)
        with self.assertRaises(RegionNotFoundException):
            self.service.create(command=self.get_valid_project_create_command(), user_id=Id(value=self.user_id))

    def test_create_with_project_max_steps(self):
        command = self.get_valid_project_create_command()
        command.steps = [
            ProjectStepCreateCommand(
                name=ProjectStepName(value="Step"),
                description=Description(value="Description"),
                date=ProjectStepDate(value=date(2077, 12, 31)),
            )
            for _ in range(PROJECT_STEPS_MAX_AMOUNT + 1)
        ]
        check_raises_in_docs(self.service.create, ProjectStepMaxAmountException)
        with self.assertRaises(ProjectStepMaxAmountException):
            self.service.create(command=command, user_id=Id(value=self.user.id))
