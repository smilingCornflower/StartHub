from datetime import date, timedelta
from typing import Any

from application.converters.request_converters.project import request_data_to_project_create_payload
from django.test import SimpleTestCase
from domain.exceptions.project_management import InvalidProjectStageException, ProjectDeadlineInPastValidationException
from domain.exceptions.validation import (
    DateIsNotIsoFormatException,
    DisallowedSocialLinkException,
    EmptyStringException,
    FirstNameIsTooLongException,
    InvalidPhoneNumberException,
    InvalidSocialLinkException,
    LastNameIsTooLongException,
    MissingRequiredFieldException,
    ValidationException,
)
from domain.value_objects.project_management import ProjectCreatePayload


class TestProjectCreatePayloadConversion(SimpleTestCase):
    def setUp(self) -> None:
        self.valid_data: dict[str, Any] = {
            "name": "Test Project",
            "description": "Project description",
            "category_id": 1,
            "company_id": 1,
            "funding_model_id": 3,
            "stage": "idea",
            "goal_sum": 10000.0,
            "deadline": (date.today() + timedelta(days=30)).isoformat(),
            "team_members": [{"first_name": "John", "last_name": "Doe", "description": "Developer"}],
            "social_links": {
                "facebook": "https://facebook.com/validuser",
                "instagram": "https://instagram.com/validuser",
            },
            "phone_number": "+77026892899",
        }
        self.user_id = 1

    def test_valid_conversion(self) -> None:
        payload = request_data_to_project_create_payload(self.valid_data, user_id=self.user_id)

        self.assertIsInstance(payload, ProjectCreatePayload)
        self.assertEqual(payload.name, self.valid_data["name"])
        self.assertEqual(payload.description, self.valid_data["description"])
        self.assertEqual(payload.category_id.value, self.valid_data["category_id"])
        self.assertEqual(payload.creator_id.value, self.user_id)
        self.assertEqual(payload.company_id.value, self.valid_data["company_id"])
        self.assertEqual(payload.funding_model_id.value, self.valid_data["funding_model_id"])
        self.assertEqual(payload.stage.value, self.valid_data["stage"])
        self.assertEqual(payload.goal_sum, self.valid_data["goal_sum"])
        self.assertEqual(payload.deadline.isoformat(), self.valid_data["deadline"])
        self.assertEqual(payload.phone_number.value, self.valid_data["phone_number"])

        # Test team members
        self.assertEqual(len(payload.team_members), len(self.valid_data["team_members"]))
        for i, member in enumerate(payload.team_members):
            self.assertEqual(member.first_name.value, self.valid_data["team_members"][i]["first_name"])
            self.assertEqual(member.last_name.value, self.valid_data["team_members"][i]["last_name"])
            self.assertEqual(member.description, self.valid_data["team_members"][i]["description"])

        # Test social links
        self.assertEqual(len(payload.social_links), len(self.valid_data["social_links"]))
        social_links_dict = {link.platform: link.link for link in payload.social_links}
        for platform, link in self.valid_data["social_links"].items():
            self.assertEqual(social_links_dict[platform], link)

    def test_missing_required_field(self) -> None:
        for field in [
            "name",
            "description",
            "category_id",
            "funding_model_id",
            "stage",
            "goal_sum",
            "deadline",
            "company_id",
            "phone_number",
            "team_members",
            "social_links",
        ]:
            with self.subTest(field=field):

                self.valid_data.pop(field)
                with self.assertRaises(MissingRequiredFieldException):
                    request_data_to_project_create_payload(self.valid_data, self.user_id)

    def test_invalid_goal_sum(self) -> None:

        self.valid_data["goal_sum"] = -100
        with self.assertRaises(ValidationException):
            request_data_to_project_create_payload(self.valid_data, self.user_id)

    def test_invalid_deadline(self) -> None:

        self.valid_data["deadline"] = (date.today() - timedelta(days=1)).isoformat()
        with self.assertRaises(ProjectDeadlineInPastValidationException):
            request_data_to_project_create_payload(self.valid_data, self.user_id)

        self.valid_data["deadline"] = "invalid-date"
        with self.assertRaises(DateIsNotIsoFormatException):
            request_data_to_project_create_payload(self.valid_data, self.user_id)

    def test_invalid_phone_number(self) -> None:

        self.valid_data["phone_number"] = "invalid-phone"
        with self.assertRaises(InvalidPhoneNumberException):
            request_data_to_project_create_payload(self.valid_data, self.user_id)

    def test_invalid_social_links(self) -> None:
        self.valid_data["social_links"] = {
            "telegram": "https://telegramm.me/smile04tnPiecesOfRoutine",
            "youtube": "https://www.yutube.com/watch?v=cvaIgq5j2Q8",
        }
        with self.assertRaises(InvalidSocialLinkException):
            request_data_to_project_create_payload(self.valid_data, self.user_id)

    def test_disallowed_social_platforms(self) -> None:
        self.valid_data["social_links"] = {
            "pinterest": "https://ru.pinterest.com/pin/31806741113659353/",
            "gpt": "https://chatgpt.com",
        }
        with self.assertRaises(DisallowedSocialLinkException):
            request_data_to_project_create_payload(self.valid_data, self.user_id)

    def test_empty_team_members(self) -> None:

        self.valid_data["team_members"] = []

        # no exceptions
        request_data_to_project_create_payload(self.valid_data, self.user_id)

    def test_invalid_team_member_data(self) -> None:
        with self.subTest("first name is too long"):
            self.valid_data["team_members"][0]["first_name"] = "A" * 256
            with self.assertRaises(FirstNameIsTooLongException):
                request_data_to_project_create_payload(self.valid_data, self.user_id)
            self.valid_data["team_members"][0]["first_name"] = "name1"

        with self.subTest("last name is too long"):
            self.valid_data["team_members"][0]["last_name"] = "A" * 256
            with self.assertRaises(LastNameIsTooLongException):
                request_data_to_project_create_payload(self.valid_data, self.user_id)
            self.valid_data["team_members"][0]["last_name"] = "surname1"

        with self.subTest("empty first name"):
            self.valid_data["team_members"][0]["first_name"] = ""
            with self.assertRaises(EmptyStringException):
                request_data_to_project_create_payload(self.valid_data, self.user_id)
            self.valid_data["team_members"][0]["first_name"] = "name1"

        with self.subTest("empty last name"):
            self.valid_data["team_members"][0]["last_name"] = ""
            with self.assertRaises(EmptyStringException):
                request_data_to_project_create_payload(self.valid_data, self.user_id)
            self.valid_data["team_members"][0]["last_name"] = "surname1"

    def test_invalid_category_id_type(self) -> None:

        self.valid_data["category_id"] = "not-an-integer"

        with self.assertRaises(ValueError):
            request_data_to_project_create_payload(self.valid_data, self.user_id)

    def test_invalid_funding_model_id_type(self) -> None:

        self.valid_data["funding_model_id"] = "not-an-integer"

        with self.assertRaises(ValueError):
            request_data_to_project_create_payload(self.valid_data, self.user_id)

    def test_invalid_stage(self) -> None:
        self.valid_data["stage"] = "invalid-stage"

        with self.assertRaises(InvalidProjectStageException):
            request_data_to_project_create_payload(self.valid_data, self.user_id)
