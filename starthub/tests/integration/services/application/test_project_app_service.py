from copy import deepcopy
from datetime import date
from typing import Any, cast

from application.service_factories.project import ProjectServiceFactory
from application.services.project import ProjectAppService
from django.test import TestCase
from domain.exceptions.company import CompanyNotFoundException, CompanyOwnershipRequiredException
from domain.exceptions.funding_model import FundingModelNotFoundException
from domain.exceptions.project import (
    NegativeProjectGoalSumValidationException,
    ProjectDeadlineInPastValidationException,
    ProjectNameIsTooLongValidationException,
)
from domain.exceptions.project_category import ProjectCategoryNotFoundException
from domain.exceptions.user import UserNotFoundException
from domain.exceptions.validation import (
    DateIsNotIsoFormatException,
    DisallowedSocialLinkException,
    EmptyStringException,
    FirstNameIsTooLongException,
    InvalidPhoneNumberException,
    InvalidSocialLinkException,
    LastNameIsTooLongException,
)
from domain.models.company import Company
from domain.models.country import Country
from domain.models.funding_model import FundingModel
from domain.models.project import Project, ProjectPhone, ProjectSocialLink, TeamMember
from domain.models.project_category import ProjectCategory
from domain.models.user import User


class TestProjectAppService(TestCase):
    service: ProjectAppService
    user: User
    country: Country
    company: Company
    category: ProjectCategory
    funding_model: FundingModel

    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = User.objects.create_user(
            email="test@example.com",
            username="testuser",
            password="Password123!",
        )
        cls.country = Country.objects.create(code="KZ")
        cls.company = Company.objects.create(
            name="My Company",
            representative_id=cls.user.id,
            description="Some description",
            country=cls.country,
            business_id="1234567890",
            established_date=date(2020, 1, 1),
        )
        cls.funding_model = FundingModel.objects.create(name="Adaptable")
        cls.category = ProjectCategory.objects.create(name="Healthcare")
        cls.service = ProjectServiceFactory.create_service()

    def setUp(self) -> None:
        self.valid_data: dict[str, Any] = {
            "name": "ProjectName",
            "description": "Description",
            "category_id": self.category.id,
            "funding_model_id": self.funding_model.id,
            "goal_sum": 100,
            "deadline": "2035-05-30",
            "team_members": [
                {"first_name": "name1", "last_name": "surname1", "description": "description1"},
                {"first_name": "name2", "last_name": "surname2", "description": "description2"},
            ],
            "company_id": self.company.id,
            "social_links": {
                "telegram": "https://t.me/smile04tnPiecesOfRoutine",
                "youtube": "https://www.youtube.com/watch?v=cvaIgq5j2Q8",
            },
            "phone_number": "+77026992839",
        }

    def test_valid_create(self) -> None:
        project: Project = self.service.create(self.valid_data, self.user.id)
        self.assertEqual(project.name, self.valid_data["name"])
        self.assertEqual(project.description, self.valid_data["description"])
        self.assertEqual(project.category.id, self.valid_data["category_id"])
        self.assertEqual(project.funding_model.id, self.valid_data["funding_model_id"])
        self.assertEqual(project.goal_sum, self.valid_data["goal_sum"])
        self.assertEqual(str(project.deadline), self.valid_data["deadline"])
        self.assertEqual(project.company.id, self.valid_data["company_id"])
        self.assertEqual(project.phones.first().number, self.valid_data["phone_number"])  # type: ignore
        self.assertEqual(project.creator.id, self.user.id)

        for s, t in zip(project.social_links.all(), self.valid_data["social_links"].items()):
            self.assertEqual(s.platform, t[0])
            self.assertEqual(s.url, t[1])

        for m, d in zip(project.team_members.all(), self.valid_data["team_members"]):
            self.assertEqual(m.name, d["first_name"])
            self.assertEqual(m.surname, d["last_name"])
            self.assertEqual(m.description, d["description"])

    def test_missing_fields(self) -> None:
        for k in self.valid_data:
            with self.subTest(missing_field=k):
                valid_data_copy = deepcopy(self.valid_data)
                valid_data_copy.pop(k)

                with self.assertRaises(KeyError):
                    self.service.create(valid_data_copy, self.user.id)

    def test_invalid_project_name(self) -> None:
        with self.subTest("project name is too long"):
            self.valid_data["name"] = "A" * 500
            with self.assertRaises(ProjectNameIsTooLongValidationException):
                self.service.create(self.valid_data, self.user.id)

        with self.subTest("empty project name"):
            self.valid_data["name"] = ""
            with self.assertRaises(EmptyStringException):
                self.service.create(self.valid_data, self.user.id)

    def test_negative_goal_sum(self) -> None:
        self.valid_data["goal_sum"] = -100
        with self.assertRaises(NegativeProjectGoalSumValidationException):
            self.service.create(self.valid_data, self.user.id)

    def test_deadline_in_past(self) -> None:
        self.valid_data["deadline"] = "2020-01-01"

        with self.assertRaises(ProjectDeadlineInPastValidationException):
            self.service.create(self.valid_data, self.user.id)

    def test_invalid_date_format(self) -> None:
        self.valid_data["deadline"] = "2020.01.01"

        with self.assertRaises(DateIsNotIsoFormatException):
            self.service.create(self.valid_data, self.user.id)

    def test_non_existing_category(self) -> None:
        self.valid_data["category_id"] = -1
        with self.assertRaises(ProjectCategoryNotFoundException):
            self.service.create(self.valid_data, self.user.id)

    def test_non_existing_funding_model(self) -> None:
        self.valid_data["funding_model_id"] = -1
        with self.assertRaises(FundingModelNotFoundException):
            self.service.create(self.valid_data, self.user.id)

    def test_non_existing_company(self) -> None:
        self.valid_data["company_id"] = -1
        with self.assertRaises(CompanyNotFoundException):
            self.service.create(self.valid_data, self.user.id)

    def test_invalid_phone_number(self) -> None:
        self.valid_data["phone_number"] = "invalid-phone"
        with self.assertRaises(InvalidPhoneNumberException):
            self.service.create(self.valid_data, self.user.id)

    def test_invalid_social_links(self) -> None:
        self.valid_data["social_links"] = {
            "telegram": "https://telegramm.me/smile04tnPiecesOfRoutine",
            "youtube": "https://www.yutube.com/watch?v=cvaIgq5j2Q8",
        }
        with self.assertRaises(InvalidSocialLinkException):
            self.service.create(self.valid_data, self.user.id)

    def test_disallowed_social_platforms(self) -> None:
        self.valid_data["social_links"] = {
            "pinterest": "https://ru.pinterest.com/pin/31806741113659353/",
            "gpt": "https://chatgpt.com",
        }
        with self.assertRaises(DisallowedSocialLinkException):
            self.service.create(self.valid_data, self.user.id)

    def test_invalid_team_members(self) -> None:
        with self.subTest("first name is too long"):
            self.valid_data["team_members"][0]["first_name"] = "A" * 256
            with self.assertRaises(FirstNameIsTooLongException):
                self.service.create(self.valid_data, self.user.id)
            self.valid_data["team_members"][0]["first_name"] = "name1"

        with self.subTest("last name is too long"):
            self.valid_data["team_members"][0]["last_name"] = "A" * 256
            with self.assertRaises(LastNameIsTooLongException):
                self.service.create(self.valid_data, self.user.id)
            self.valid_data["team_members"][0]["last_name"] = "surname1"

        with self.subTest("empty first name"):
            self.valid_data["team_members"][0]["first_name"] = ""
            with self.assertRaises(EmptyStringException):
                self.service.create(self.valid_data, self.user.id)
            self.valid_data["team_members"][0]["first_name"] = "name1"

        with self.subTest("empty last name"):
            self.valid_data["team_members"][0]["last_name"] = ""
            with self.assertRaises(EmptyStringException):
                self.service.create(self.valid_data, self.user.id)
            self.valid_data["team_members"][0]["last_name"] = "surname1"

    def test_transaction_atomicity_on_failure(self) -> None:
        self.valid_data["social_links"] = {
            "telegram": "https://telegramm.me/smile04tnPiecesOfRoutine",
            "youtube": "https://www.yutube.com/watch?v=cvaIgq5j2Q8",
        }
        try:
            self.service.create(self.valid_data, self.user.id)
        except InvalidSocialLinkException:
            pass
        self.assertEqual(Project.objects.count(), 0)
        self.assertEqual(TeamMember.objects.count(), 0)
        self.assertEqual(ProjectPhone.objects.count(), 0)
        self.assertEqual(ProjectSocialLink.objects.count(), 0)

    def test_non_existing_user_id(self) -> None:
        with self.assertRaises(UserNotFoundException):
            self.service.create(self.valid_data, user_id=-1)

    def test_user_is_not_company_representative(self) -> None:
        another_user = User.objects.create_user(
            email="another@example.com",
            username="another",
            password="Password123!",
        )
        with self.assertRaises(CompanyOwnershipRequiredException):
            self.service.create(self.valid_data, user_id=another_user.id)
