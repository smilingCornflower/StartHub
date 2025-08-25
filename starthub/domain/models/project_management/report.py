from django.db import models
from domain.models.base import BaseModel


class ProjectReport(BaseModel):
    project = models.ForeignKey("domain.Project", on_delete=models.CASCADE, related_name="reports")
    report = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Report to Project(id={self.project_id}): {self.report[:50]}..."

    @classmethod
    def get_permission_key(cls) -> str:
        return "project_reports"
