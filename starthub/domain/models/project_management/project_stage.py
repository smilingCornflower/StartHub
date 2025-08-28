from autoslug import AutoSlugField
from django.db import models
from domain.constants import CHAR_FIELD_MEDIUM_LENGTH, DESCRIPTION_MAX_LENGTH
from domain.models.base import BaseModel


class ProjectStage(BaseModel):
    name = models.CharField(max_length=CHAR_FIELD_MEDIUM_LENGTH)
    slug = AutoSlugField(populate_from="name", unique=True, max_length=CHAR_FIELD_MEDIUM_LENGTH + 10)
    description = models.CharField(max_length=DESCRIPTION_MAX_LENGTH, null=True)

    class Meta:
        db_table = "project_stages"

    def __str__(self) -> str:
        return self.name

    @classmethod
    def get_permission_key(cls) -> str:
        return "project_stage"
