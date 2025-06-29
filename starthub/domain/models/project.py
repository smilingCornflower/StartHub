from autoslug import AutoSlugField
from django.db import models
from domain.constants import (
    CHAR_FIELD_MAX_LENGTH,
    CHAR_FIELD_MEDIUM_LENGTH,
    CHAR_FIELD_SHORT_LENGTH,
    FUNDING_GOAL_MAX_DIGITS,
)
from domain.enums.project_stage import ProjectStageEnum
from domain.enums.project_status import ProjectStatusEnum
from domain.models.base import BaseModel


class Project(BaseModel):

    name = models.CharField(max_length=CHAR_FIELD_MAX_LENGTH)
    slug = AutoSlugField(populate_from="name", unique=True, max_length=CHAR_FIELD_MAX_LENGTH)
    description = models.TextField()
    category = models.ForeignKey("domain.ProjectCategory", on_delete=models.PROTECT)
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

    def __str__(self) -> str:
        return self.name

    class Meta:
        db_table = "projects"

    @classmethod
    def get_permission_key(cls) -> str:
        return "project"


class TeamMember(BaseModel):
    project = models.ForeignKey("domain.Project", on_delete=models.CASCADE, related_name="team_members")
    name = models.CharField(max_length=CHAR_FIELD_SHORT_LENGTH)
    surname = models.CharField(max_length=CHAR_FIELD_SHORT_LENGTH)
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "team_members"

    def __str__(self) -> str:
        return f"{self.name} {self.surname}"

    @classmethod
    def get_permission_key(cls) -> str:
        return "project_team_member"


class ProjectSocialLink(BaseModel):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="social_links")
    platform = models.CharField(max_length=CHAR_FIELD_MEDIUM_LENGTH)
    url = models.URLField()

    class Meta:
        db_table = "project_social_links"
        unique_together = ("project", "platform")

    def __str__(self) -> str:
        return f"{self.project.name} {self.platform}"

    @classmethod
    def get_permission_key(cls) -> str:
        return "project_social_link"


class ProjectPhone(BaseModel):
    project = models.ForeignKey("domain.Project", on_delete=models.CASCADE, related_name="phones")
    number = models.CharField(max_length=CHAR_FIELD_SHORT_LENGTH)

    class Meta:
        db_table = "project_phones"
        unique_together = ("project", "number")

    def __str__(self) -> str:
        return f"{self.project.name} {self.number}"

    @classmethod
    def get_permission_key(cls) -> str:
        return "project_phone"


class ProjectImage(BaseModel):
    project = models.ForeignKey("domain.Project", on_delete=models.CASCADE, related_name="images")
    file_path = models.CharField(max_length=CHAR_FIELD_MAX_LENGTH)
    order = models.SmallIntegerField()

    class Meta:
        db_table = "project_images"

    def __str__(self) -> str:
        return self.file_path

    @classmethod
    def get_permission_key(cls) -> str:
        return "project_image"
