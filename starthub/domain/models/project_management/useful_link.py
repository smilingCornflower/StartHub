from django.db import models
from domain.constants import CHAR_FIELD_MEDIUM_LENGTH
from domain.models.base import BaseModel
from domain.models.project_management.project import Project


class ProjectUsefulLink(BaseModel):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="useful_links")
    name = models.CharField(max_length=CHAR_FIELD_MEDIUM_LENGTH)
    url = models.URLField()

    class Meta:
        db_table = "project_useful_links"
        unique_together = ("project", "url")

    def __str__(self) -> str:
        return f"UsefulLink: {self.url}"

    @classmethod
    def get_permission_key(cls) -> str:
        return "project_useful_link"
