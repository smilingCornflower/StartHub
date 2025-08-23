from django.db import models

from domain.constants import CHAR_FIELD_SHORT_LENGTH
from domain.models.base import BaseModel


class ProjectPhone(BaseModel):
    project = models.ForeignKey("domain.Project", on_delete=models.CASCADE, related_name="phones")
    number = models.CharField(max_length=CHAR_FIELD_SHORT_LENGTH)

    class Meta:
        db_table = "project_phones"
        unique_together = ("project", "number")

    def __str__(self) -> str:
        return f"{self.project.name} {self.number}"

    @classmethod
    def get_permission_key(cls) -> str:
        return "project_phone"
