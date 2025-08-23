from django.db import models

from domain.constants import CHAR_FIELD_MAX_LENGTH
from domain.models.base import BaseModel


class ProjectMedia(BaseModel):
    project = models.ForeignKey("domain.Project", on_delete=models.CASCADE, related_name="media")
    file_path = models.CharField(max_length=CHAR_FIELD_MAX_LENGTH)
    order = models.SmallIntegerField()

    class Meta:
        db_table = "project_media"

    def __str__(self) -> str:
        return self.file_path

    @classmethod
    def get_permission_key(cls) -> str:
        return "project_media"
