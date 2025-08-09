from autoslug import AutoSlugField
from django.db import models
from domain.constants import CHAR_FIELD_MAX_LENGTH, FUNDING_GOAL_MAX_DIGITS
from domain.models.base import BaseModel


class ProjectCrowdfunding(BaseModel):
    project = models.OneToOneField("domain.Project", on_delete=models.CASCADE, related_name="crowdfunding")
    name = models.CharField(max_length=CHAR_FIELD_MAX_LENGTH)
    slug = AutoSlugField(populate_from="name", unique=True, max_length=CHAR_FIELD_MAX_LENGTH)
    amount = models.DecimalField(max_digits=FUNDING_GOAL_MAX_DIGITS, decimal_places=2)

    class Meta:
        db_table = "project_crowdfundings"

    def __str__(self) -> str:
        return self.name

    @classmethod
    def get_permission_key(cls) -> str:
        return "project_crowdfunding"
