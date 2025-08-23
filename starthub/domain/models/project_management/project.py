from autoslug import AutoSlugField
from django.db import models

from domain.constants import CHAR_FIELD_MAX_LENGTH, CHAR_FIELD_SHORT_LENGTH, FUNDING_GOAL_MAX_DIGITS
from domain.enums.project_stage import ProjectStageEnum
from domain.enums.project_status import ProjectStatusEnum
from domain.models.base import BaseModel


class Project(BaseModel):
    name = models.CharField(max_length=CHAR_FIELD_MAX_LENGTH)
    slug = AutoSlugField(populate_from="name", unique=True, max_length=CHAR_FIELD_MAX_LENGTH)
    goal_description = models.TextField(blank=True, null=True)
    description = models.TextField()
    categories = models.ManyToManyField("domain.ProjectCategory", related_name="projects")
    creator = models.ForeignKey("domain.User", on_delete=models.PROTECT, related_name="created_projects")
    funding_model = models.ForeignKey("domain.FundingModel", on_delete=models.PROTECT)

    stage = models.CharField(max_length=16, choices=[(i.value, i.name) for i in ProjectStageEnum])
    status = models.CharField(
        max_length=CHAR_FIELD_SHORT_LENGTH, choices=[(i.value, i.name) for i in ProjectStatusEnum]
    )

    goal_sum = models.DecimalField(max_digits=FUNDING_GOAL_MAX_DIGITS, decimal_places=2)
    current_sum = models.DecimalField(max_digits=FUNDING_GOAL_MAX_DIGITS, decimal_places=2, default=0)
    deadline = models.DateField()
    plan = models.CharField(max_length=CHAR_FIELD_MAX_LENGTH, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    ltv = models.FloatField(null=True)
    arpu = models.FloatField(null=True)
    arppu = models.FloatField(null=True)
    cac = models.FloatField(null=True)
    nps = models.FloatField(null=True)
    roi = models.FloatField(null=True)
    aov = models.FloatField(null=True)
    churn_rate = models.FloatField(null=True)
    retention_rate = models.FloatField(null=True)
    conversion_rate = models.FloatField(null=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        db_table = "projects"

    @classmethod
    def get_permission_key(cls) -> str:
        return "project"

    STATUS_FIELD = "status"
    STATUS_UNDER_MODERATION_FIELD = f"status.{ProjectStatusEnum.UNDER_MODERATION}"
    STATUS_REJECTED_FIELD = f"status.{ProjectStatusEnum.REJECTED}"
    STATUS_CANCELLED_FIELD = f"status.{ProjectStatusEnum.CANCELLED}"
