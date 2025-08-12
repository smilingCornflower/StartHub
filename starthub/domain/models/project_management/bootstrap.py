from domain.models.base import BaseModel
from django.db import models
from domain.constants import CHAR_FIELD_MAX_LENGTH


class ProjectBootstrap(BaseModel):
    project = models.ForeignKey("domain.Project", on_delete=models.CASCADE, related_name="bootstraps")
    description = models.CharField(max_length=CHAR_FIELD_MAX_LENGTH)

    class Meta:
        db_table = "project_bootstraps"

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(project_id={self.project_id})"

    @classmethod
    def get_permission_key(cls) -> str:
        return "project_bootstrap"