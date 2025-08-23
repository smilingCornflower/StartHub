from django.db import models

from domain.constants import CHAR_FIELD_SHORT_LENGTH
from domain.models.base import BaseModel


class TeamMember(BaseModel):
    project = models.ForeignKey("domain.Project", on_delete=models.CASCADE, related_name="team_members")
    name = models.CharField(max_length=CHAR_FIELD_SHORT_LENGTH)
    surname = models.CharField(max_length=CHAR_FIELD_SHORT_LENGTH)
    description = models.TextField(blank=True, null=True)
    # TODO: position (one or more)
    # TODO: phone (optional)

    class Meta:
        db_table = "team_members"

    def __str__(self) -> str:
        return f"{self.name} {self.surname}"

    @classmethod
    def get_permission_key(cls) -> str:
        return "project_team_member"
