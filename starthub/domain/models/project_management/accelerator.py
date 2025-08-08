from django.db import models
from domain.constants import CHAR_FIELD_MAX_LENGTH
from domain.models.base import BaseModel


class ProjectAccelerator(BaseModel):
    project = models.OneToOneField("domain.Project", on_delete=models.CASCADE, related_name="accelerator")
    name = models.CharField(max_length=CHAR_FIELD_MAX_LENGTH)
    description = models.TextField()

    class Meta:
        db_table = "project_accelerators"

    def __str__(self) -> str:
        return self.name

    @classmethod
    def get_permission_key(cls) -> str:
        return "accelerator"
