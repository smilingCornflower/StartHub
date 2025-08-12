from autoslug import AutoSlugField
from django.db import models
from domain.constants import CHAR_FIELD_MAX_LENGTH
from domain.models.base import BaseModel


class ProjectGovernmentGrant(BaseModel):
    name = models.CharField(max_length=CHAR_FIELD_MAX_LENGTH)
    name_slug = AutoSlugField(populate_from="name", unique=True, max_length=CHAR_FIELD_MAX_LENGTH)

    amount = models.FloatField()
    organization_name = models.CharField(max_length=CHAR_FIELD_MAX_LENGTH)
    organization_name_slug = AutoSlugField(populate_from="name", unique=True, max_length=CHAR_FIELD_MAX_LENGTH)

    class Meta:
        db_table = "project_government_grants"

    def __str__(self) -> str:
        return f"{self.organization_name} {self.name}"

    @classmethod
    def get_permission_key(cls) -> str:
        return "project_government_grant"
