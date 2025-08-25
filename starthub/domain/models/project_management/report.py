from django.db import models
from domain.models.base import BaseModel


class ProjectReport(BaseModel):
    project = models.ForeignKey("domain.Project", on_delete=models.CASCADE, related_name="reports")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "project_reports"

    def __str__(self) -> str:
        return f"Report to Project(id={self.project_id}): {self.content[:50]}..."

    @classmethod
    def get_permission_key(cls) -> str:
        return "project_reports"
