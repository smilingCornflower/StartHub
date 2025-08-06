from django.db import models
from domain.constants import CHAR_FIELD_MEDIUM_LENGTH
from domain.models.base import BaseModel


class ProjectStep(BaseModel):
    name = models.CharField(max_length=CHAR_FIELD_MEDIUM_LENGTH)
    description = models.TextField()
    date = models.DateField()

    def __str__(self) -> str:
        return self.name

    @classmethod
    def get_permission_key(cls) -> str:
        return "project_step"
