from autoslug import AutoSlugField
from django.db import models
from domain.constants import (
    CHAR_FIELD_MAX_LENGTH,
    CHAR_FIELD_MEDIUM_LENGTH,
    CHAR_FIELD_SHORT_LENGTH,
    FUNDING_GOAL_MAX_DIGITS,
)
from domain.models.base import BaseModel


class Project(BaseModel):
    name = models.CharField(max_length=CHAR_FIELD_MAX_LENGTH, unique=True)
    slug = AutoSlugField(populate_from="name", unique=True, max_length=CHAR_FIELD_MAX_LENGTH)
    description = models.TextField()
    category = models.ForeignKey("domain.ProjectCategory", on_delete=models.PROTECT)

    creator = models.ForeignKey("domain.User", on_delete=models.PROTECT, related_name="created_projects")
    team = models.ManyToManyField("domain.TeamMember")

    funding_model = models.ForeignKey("domain.FundingModel", on_delete=models.PROTECT)
    goal_sum = models.DecimalField(max_digits=FUNDING_GOAL_MAX_DIGITS, decimal_places=2)
    current_sum = models.DecimalField(max_digits=FUNDING_GOAL_MAX_DIGITS, decimal_places=2, default=0)
    deadline = models.DateField()

    is_active = models.BooleanField(default=True)
    # TODO: ProjectPhoto

    def __str__(self) -> str:
        return self.name


class TeamMember(BaseModel):
    company = models.ForeignKey("domain.Company", on_delete=models.CASCADE, related_name="team_members")
    name = models.CharField(max_length=CHAR_FIELD_SHORT_LENGTH)
    surname = models.CharField(max_length=CHAR_FIELD_MEDIUM_LENGTH)
    description = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.name} {self.surname}"
