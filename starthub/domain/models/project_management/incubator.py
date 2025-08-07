from django.db import models
from domain.constants import CHAR_FIELD_MAX_LENGTH
from domain.models.base import BaseModel


class ProjectIncubator(BaseModel):
    project = models.OneToOneField("domain.Project", on_delete=models.CASCADE)
    name = models.CharField(max_length=CHAR_FIELD_MAX_LENGTH)
    description = models.TextField()

    class Meta:
        db_table = "project_incubators"

    def __str__(self) -> str:
        return self.name

    @classmethod
    def get_permission_key(cls) -> str:
        return "project_incubator"
