import json
from datetime import date, timedelta
from pathlib import Path
from typing import Any

import pydantic
from application.converters.request_converters.project import request_data_to_project_create_command
from config.settings import BASE_DIR
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import SimpleTestCase
from domain.exceptions.project_management import (
    InvalidProjectStageException,
    NegativeProjectGoalSumValidationException,
    ProjectDeadlineInPastValidationException,
)
from domain.exceptions.validation import (
    DateInFutureException,
    DateIsNotIsoFormatException,
    DisallowedSocialLinkException,
    EmptyStringException,
    FirstNameIsTooLongException,
    InvalidPhoneNumberException,
    InvalidSocialLinkException,
    LastNameIsTooLongException,
    MissingRequiredFieldException,
)
from domain.value_objects.project_management import ProjectCreateCommand


class TestProjectCreateCommandConversion(SimpleTestCase):
    def setUp(self) -> None:
        pdf_file: Path = BASE_DIR / "tests/files/The_C_Programming_Language.pdf"

        with open(pdf_file, "rb") as f:
            pdf_data: bytes = f.read()

        simple_pdf = SimpleUploadedFile(
            name="project_plan.pdf",
            content=pdf_data,
            content_type="application/pdf",
        )
        self.files = {"project_plan": simple_pdf}

        self.valid_data = {
            "project": {
                "name": "AI Startup Project",
                "description": "Innovative AI solution for small businesses",
                "category_id": 1,
                "funding_model_id": 2,
                "deadline": (date.today() + timedelta(days=90)).isoformat(),
                "stage": "idea",
                "goal_sum": 1700000.00,
                "phone_number": "+77026882938",
                "social_links": {
                    "telegram": "https://t.me/smile04tnPiecesOfRoutine",
                    "youtube": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                },
            },
            "company": {
                "name": "AI Innovations Inc.",
                "country_code": "KZ",
                "business_id": "123456789012",
                "established_date": "2020-01-15",
            },
            "company_founder": {"first_name": "John", "last_name": "Doe", "description": "Founder and CEO"},
            "team_members": [
                {"first_name": "Jane", "last_name": "Smith", "description": "CTO"},
                {"first_name": "Mike", "last_name": "Johnson", "description": "Lead Developer"},
            ],
        }

        self.user_id = 1

    def prepare_data(self, data: dict[str, Any]) -> dict[str, str]:
        return {k: json.dumps(v) for k, v in data.items()}

    def check_raises(self, exc: type[Exception]) -> None:
        self.assertTrue(f":raises {exc.__name__}:" in request_data_to_project_create_command.__doc__)

    def test_valid_conversion(self) -> None:
        command = request_data_to_project_create_command(
            self.prepare_data(self.valid_data), self.files, user_id=self.user_id
        )
        self.assertEqual(type(command), ProjectCreateCommand)
        self.assertEqual(command.name.value, self.valid_data["project"]["name"])
        self.assertEqual(command.description.value, self.valid_data["project"]["description"])
        self.assertEqual(command.category_id.value, self.valid_data["project"]["category_id"])
        self.assertEqual(command.creator_id.value, self.user_id)
        self.assertEqual(command.funding_model_id.value, self.valid_data["project"]["funding_model_id"])
        self.assertEqual(command.stage.value, self.valid_data["project"]["stage"])
        self.assertEqual(command.goal_sum.value, self.valid_data["project"]["goal_sum"])
        self.assertEqual(command.deadline.value.isoformat(), self.valid_data["project"]["deadline"])
        self.assertEqual(command.phone_number.value, self.valid_data["project"]["phone_number"])
        self.assertTrue(isinstance(command.plan_file.value, bytes))

        # Team members
        self.assertEqual(len(command.team_members), len(self.valid_data["team_members"]))
        for i, member in enumerate(command.team_members):
            self.assertEqual(member.first_name.value, self.valid_data["team_members"][i]["first_name"])
            self.assertEqual(member.last_name.value, self.valid_data["team_members"][i]["last_name"])
            self.assertEqual(member.description.value, self.valid_data["team_members"][i]["description"])

        # Social links
        self.assertEqual(len(command.social_links), len(self.valid_data["project"]["social_links"]))
        social_links_dict = {link.platform: link.link for link in command.social_links}
        for platform, link in self.valid_data["project"]["social_links"].items():
            self.assertEqual(social_links_dict[platform], link)

        # Company
        self.assertEqual(command.company_name.value, self.valid_data["company"]["name"])
        self.assertEqual(command.country_code.value, self.valid_data["company"]["country_code"])
        self.assertEqual(
            command.established_date.value.isoformat(), self.valid_data["company"]["established_date"]
        )
        self.assertEqual(command.business_id.value, self.valid_data["company"]["business_id"])
        self.assertEqual(
            command.company_founder.name.value, self.valid_data["company_founder"]["first_name"]
        )
        self.assertEqual(
            command.company_founder.surname.value, self.valid_data["company_founder"]["last_name"]
        )
        self.assertEqual(
            command.company_founder.description.value, self.valid_data["company_founder"]["description"]
        )

    def test_missing_required_field(self) -> None:
        required_fields = [
            "project",
            "company",
            "company_founder",
            "team_members",
        ]

        project_required_fields = [
            "name",
            "description",
            "category_id",
            "funding_model_id",
            "stage",
            "goal_sum",
            "phone_number",
            "social_links",
        ]

        company_required_fields = [
            "name",
            "country_code",
            "business_id",
            "established_date",
        ]

        founder_required_fields = [
            "first_name",
            "last_name",
        ]

        for field in required_fields:
            with self.subTest(f"missing top-level field: {field}"):
                invalid_data = self.valid_data.copy()
                invalid_data.pop(field)
                with self.assertRaises(MissingRequiredFieldException):
                    request_data_to_project_create_command(self.prepare_data(invalid_data), self.files, self.user_id)

        for field in project_required_fields:
            with self.subTest(f"missing project field: {field}"):
                invalid_data = self.valid_data.copy()
                invalid_data["project"] = self.valid_data["project"].copy()
                invalid_data["project"].pop(field)
                with self.assertRaises(MissingRequiredFieldException):
                    request_data_to_project_create_command(self.prepare_data(invalid_data), self.files, self.user_id)

        for field in company_required_fields:
            with self.subTest(f"missing company field: {field}"):
                invalid_data = self.valid_data.copy()
                invalid_data["company"] = self.valid_data["company"].copy()
                invalid_data["company"].pop(field)
                with self.assertRaises(MissingRequiredFieldException):
                    request_data_to_project_create_command(self.prepare_data(invalid_data), self.files, self.user_id)

        for field in founder_required_fields:
            with self.subTest(f"missing founder field: {field}"):
                invalid_data = self.valid_data.copy()
                invalid_data["company_founder"] = self.valid_data["company_founder"].copy()
                invalid_data["company_founder"].pop(field)
                with self.assertRaises(MissingRequiredFieldException):
                    request_data_to_project_create_command(self.prepare_data(invalid_data), self.files, self.user_id)

        with self.subTest("missing project_plan file"):
            with self.assertRaises(MissingRequiredFieldException):
                request_data_to_project_create_command(self.prepare_data(self.valid_data), {}, self.user_id)
        self.check_raises(MissingRequiredFieldException)

    def test_invalid_goal_sum(self) -> None:
        self.valid_data["project"]["goal_sum"] = -100  # type: ignore
        with self.assertRaises(NegativeProjectGoalSumValidationException):
            request_data_to_project_create_command(self.prepare_data(self.valid_data), self.files, self.user_id)
        self.check_raises(NegativeProjectGoalSumValidationException)

    def test_invalid_deadline(self) -> None:
        self.valid_data["project"]["deadline"] = (date.today() - timedelta(days=1)).isoformat()
        with self.assertRaises(ProjectDeadlineInPastValidationException):
            request_data_to_project_create_command(
                self.prepare_data(self.valid_data), files=self.files, user_id=self.user_id
            )

            self.check_raises(ProjectDeadlineInPastValidationException)

        self.valid_data["project"]["deadline"] = "invalid-date"
        with self.assertRaises(DateIsNotIsoFormatException):
            request_data_to_project_create_command(self.prepare_data(self.valid_data), self.files, self.user_id)

        self.check_raises(DateIsNotIsoFormatException)

    def test_invalid_phone_number(self) -> None:
        self.valid_data["project"]["phone_number"] = "invalid-phone"
        with self.assertRaises(InvalidPhoneNumberException):
            request_data_to_project_create_command(self.prepare_data(self.valid_data), self.files, self.user_id)

        self.check_raises(InvalidPhoneNumberException)

    def test_invalid_social_links(self) -> None:
        self.valid_data["project"]["social_links"] = {
            "telegram": "https://telegramm.me/smile04tnPiecesOfRoutine",
            "youtube": "https://www.yutube.com/watch?v=cvaIgq5j2Q8",
        }
        with self.assertRaises(InvalidSocialLinkException):
            request_data_to_project_create_command(self.prepare_data(self.valid_data), self.files, self.user_id)

        self.check_raises(InvalidSocialLinkException)

    def test_invalid_project_stage(self) -> None:
        self.valid_data["project"]["stage"] = "invalid"

        with self.assertRaises(InvalidProjectStageException):
            request_data_to_project_create_command(self.prepare_data(self.valid_data), self.files, self.user_id)

        self.check_raises(InvalidProjectStageException)

    def test_disallowed_social_platforms(self) -> None:
        self.valid_data["project"]["social_links"] = {
            "pinterest": "https://ru.pinterest.com/pin/31806741113659353/",
            "gpt": "https://chatgpt.com",
        }
        with self.assertRaises(DisallowedSocialLinkException):
            request_data_to_project_create_command(self.prepare_data(self.valid_data), self.files, self.user_id)

        self.check_raises(DisallowedSocialLinkException)

    def test_empty_team_members(self) -> None:
        self.valid_data["team_members"] = []

        # no exceptions
        request_data_to_project_create_command(self.prepare_data(self.valid_data), self.files, self.user_id)

    def test_invalid_team_member_data(self) -> None:
        with self.subTest("first name is too long"):
            self.valid_data["team_members"][0]["first_name"] = "A" * 256
            with self.assertRaises(FirstNameIsTooLongException):
                request_data_to_project_create_command(self.prepare_data(self.valid_data), self.files, self.user_id)
            self.valid_data["team_members"][0]["first_name"] = "name1"

        with self.subTest("last name is too long"):
            self.valid_data["team_members"][0]["last_name"] = "A" * 256
            with self.assertRaises(LastNameIsTooLongException):
                request_data_to_project_create_command(self.prepare_data(self.valid_data), self.files, self.user_id)
            self.valid_data["team_members"][0]["last_name"] = "surname1"

        with self.subTest("empty first name"):
            self.valid_data["team_members"][0]["first_name"] = ""
            with self.assertRaises(EmptyStringException):
                request_data_to_project_create_command(self.prepare_data(self.valid_data), self.files, self.user_id)
            self.valid_data["team_members"][0]["first_name"] = "name1"

        with self.subTest("empty last name"):
            self.valid_data["team_members"][0]["last_name"] = ""
            with self.assertRaises(EmptyStringException):
                request_data_to_project_create_command(self.prepare_data(self.valid_data), self.files, self.user_id)
            self.valid_data["team_members"][0]["last_name"] = "surname1"

        self.check_raises(EmptyStringException)
        self.check_raises(LastNameIsTooLongException)
        self.check_raises(FirstNameIsTooLongException)

    def test_invalid_category_id_type(self) -> None:

        self.valid_data["project"]["category_id"] = "not-an-integer"

        with self.assertRaises(pydantic.ValidationError):
            request_data_to_project_create_command(self.prepare_data(self.valid_data), self.files, self.user_id)
        self.check_raises(pydantic.ValidationError)

    def test_invalid_funding_model_id_type(self) -> None:
        self.valid_data["project"]["funding_model_id"] = "not-an-integer"

        with self.assertRaises(pydantic.ValidationError):
            request_data_to_project_create_command(self.prepare_data(self.valid_data), self.files, self.user_id)

        self.check_raises(pydantic.ValidationError)

    def test_rejects_invalid_date_formats(self) -> None:
        invalid_formats = [
            "01.01.2020",
            "01/01/2020",
            "01-Jan-2020",
            "2020-1-1",
            "20-01-01",
            "2020-13-01",
            "2020-01-32",
        ]

        for date_str in invalid_formats:
            with self.subTest(date_format=date_str):
                test_data = self.valid_data.copy()
                test_data["company"]["established_date"] = date_str  # type: ignore
                with self.assertRaises(DateIsNotIsoFormatException):
                    request_data_to_project_create_command(self.prepare_data(test_data), self.files, self.user_id)  # type: ignore

    def test_rejects_company_established_future_dates(self) -> None:
        future_dates = [
            (date.today() + timedelta(days=1)).isoformat(),
            (date.today().replace(year=date.today().year + 1)).isoformat(),
            "2030-01-01",
        ]

        for future_date in future_dates:
            test_data = self.valid_data.copy()
            test_data["company"]["established_date"] = future_date  # type: ignore
            with self.assertRaises(DateInFutureException):
                request_data_to_project_create_command(self.prepare_data(test_data), self.files, self.user_id)  # type: ignore
            self.check_raises(DateInFutureException)
