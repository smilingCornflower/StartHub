from typing import Any

from django.test import SimpleTestCase
from domain.value_objects.common import FirstName, Id, LastName
from domain.value_objects.project_management import TeamMemberCreatePayload, TeamMemberInProjectCreatePayload
from pydantic import ValidationError


class TeamMemberPayloadTest(SimpleTestCase):
    def test_valid_team_member_create_payload(self) -> None:
        valid_data: dict[str, Any] = {
            "project_id": Id(value=1),
            "first_name": FirstName(value="John"),
            "last_name": LastName(value="Doe"),
            "description": "Senior Developer",
        }

        payload: TeamMemberCreatePayload = TeamMemberCreatePayload(**valid_data)
        self.assertEqual(payload.project_id.value, valid_data["project_id"].value)
        self.assertEqual(payload.first_name.value, valid_data["first_name"].value)
        self.assertEqual(payload.last_name.value, valid_data["last_name"].value)
        self.assertEqual(payload.description, valid_data["description"])

    def test_invalid_team_member_create_payload(self) -> None:
        invalid_cases: list[dict[str, Any]] = [
            {"first_name": FirstName(value="J"), "last_name": LastName(value="D")},
            {"project_id": "invalid-id", "first_name": FirstName(value="J"), "last_name": LastName(value="D")},
            {"project_id": Id(value=2), "last_name": LastName(value="Doe")},
            {"project_id": Id(value=3), "first_name": FirstName(value="John")},
        ]

        for case in invalid_cases:
            with self.subTest(case=case):
                with self.assertRaises(ValidationError):
                    TeamMemberCreatePayload(**case)

    def test_valid_team_member_in_project_payload(self) -> None:
        valid_data: dict[str, Any] = {
            "first_name": FirstName(value="Jane"),
            "last_name": LastName(value="Smith"),
            "description": "UI/UX Designer",
        }

        payload: TeamMemberInProjectCreatePayload = TeamMemberInProjectCreatePayload(**valid_data)
        self.assertEqual(payload.first_name.value, valid_data["first_name"].value)
        self.assertEqual(payload.last_name.value, valid_data["last_name"].value)
        self.assertEqual(payload.description, valid_data["description"])

    def test_invalid_team_member_in_project_payload(self) -> None:
        invalid_cases: list[dict[str, Any]] = [
            {"first_name": FirstName(value="Jane")},
            {"last_name": LastName(value="Smith")},
            {"description": 47},
        ]

        for case in invalid_cases:
            with self.subTest(case=case):
                with self.assertRaises(ValidationError):
                    TeamMemberInProjectCreatePayload(**case)
