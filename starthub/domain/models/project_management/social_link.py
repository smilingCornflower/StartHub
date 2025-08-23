from django.db import models

from domain.constants import CHAR_FIELD_MEDIUM_LENGTH
from domain.models.base import BaseModel
from domain.models.project_management.project import Project


class ProjectSocialLink(BaseModel):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="social_links")
    platform = models.CharField(max_length=CHAR_FIELD_MEDIUM_LENGTH)
    url = models.URLField()

    class Meta:
        db_table = "project_social_links"
        unique_together = ("project", "platform")

    def __str__(self) -> str:
        return f"{self.project.name} {self.platform}"

    @classmethod
    def get_permission_key(cls) -> str:
        return "project_social_link"
