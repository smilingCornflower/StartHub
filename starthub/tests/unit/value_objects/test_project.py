from datetime import date, timedelta
from typing import Any

from django.test import TestCase
from domain.exceptions.validation import ValidationException
from domain.value_objects.common import FirstName, Id, LastName, PhoneNumber, SocialLink
from domain.value_objects.project_management import ProjectCreatePayload, TeamMemberInProjectCreatePayload
from pydantic import ValidationError


class ProjectCreatePayloadTests(TestCase):
    def setUp(self) -> None:
        self.valid_data: dict[str, Any] = {
            "name": "Test Project",
            "description": "Test Description",
            "category_id": Id(value=1),
            "creator_id": Id(value=2),
            "funding_model_id": Id(value=3),
            "goal_sum": 1000.0,
            "deadline": date.today() + timedelta(days=30),
            "team_members": [
                TeamMemberInProjectCreatePayload(
                    first_name=FirstName(value="John"), last_name=LastName(value="Doe"), description="Developer"
                )
            ],
            "company_id": Id(value=1),
            "social_links": [SocialLink(platform="facebook", link="https://facebook.com/validprofile")],
            "phone_number": PhoneNumber(value="+77001234567"),
        }

    def test_valid_payload(self) -> None:
        payload = ProjectCreatePayload(**self.valid_data)
        self.assertEqual(payload.name, "Test Project")
        self.assertEqual(payload.category_id.value, 1)
        self.assertEqual(payload.creator_id.value, 2)
        self.assertEqual(payload.funding_model_id.value, 3)
        self.assertEqual(payload.team_members[0].first_name.value, "John")
        self.assertEqual(payload.company_id.value, 1)

    def test_goal_sum_validation(self) -> None:
        test_cases = [0, -100, -0.01]
        for value in test_cases:
            with self.subTest(value=value):
                invalid_data = self.valid_data.copy()
                invalid_data["goal_sum"] = value
                with self.assertRaises(ValidationException):
                    ProjectCreatePayload(**invalid_data)

    def test_deadline_validation(self) -> None:
        test_cases = [date.today(), date.today() - timedelta(days=1), date(1970, 1, 1)]
        for value in test_cases:
            with self.subTest(value=value):
                invalid_data = self.valid_data.copy()
                invalid_data["deadline"] = value
                with self.assertRaises(ValidationException):
                    ProjectCreatePayload(**invalid_data)

    def test_required_fields(self) -> None:
        required_fields = self.valid_data.keys()
        for field in required_fields:
            with self.subTest(field=field):
                invalid_data: dict[str, Any] = self.valid_data.copy()
                invalid_data.pop(field)
                with self.assertRaises(ValidationError):
                    ProjectCreatePayload(**invalid_data)
