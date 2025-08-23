from django.db import models

from domain.constants import CHAR_FIELD_MAX_LENGTH
from domain.models.base import BaseModel


class ProjectFile(BaseModel):
    project = models.ForeignKey("domain.Project", on_delete=models.CASCADE, related_name="files")
    file_path = models.CharField(max_length=CHAR_FIELD_MAX_LENGTH)
    name = models.CharField(max_length=CHAR_FIELD_MAX_LENGTH, null=True)

    class Meta:
        db_table = "project_files"

    def __str__(self) -> str:
        return f"Project(id={self.project_id}) - {self.file_path}"

    @classmethod
    def get_permission_key(cls) -> str:
        return "project_file"
