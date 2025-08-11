from django.db import models
from domain.constants import CHAR_FIELD_MAX_LENGTH, CHAR_FIELD_MEDIUM_LENGTH
from domain.models.base import BaseModel
from autoslug import AutoSlugField

class ProjectInvestment(BaseModel):
    project = models.ForeignKey("domain.Project", on_delete=models.CASCADE, related_name="investments")
    organization_name = models.CharField(max_length=CHAR_FIELD_MAX_LENGTH)
    slug = AutoSlugField(populate_from="organization_name", unique=True, max_length=CHAR_FIELD_MAX_LENGTH)
    amount = models.FloatField()

    class Meta:
        db_table = "project_investments"

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(project={self.project})"

    @classmethod
    def get_permission_key(cls) -> str:
        return "project_investment"


class ProjectInvestmentSocialLink(BaseModel):
    investment = models.ForeignKey("domain.ProjectInvestment", on_delete=models.CASCADE, related_name="social_links")
    platform = models.CharField(max_length=CHAR_FIELD_MEDIUM_LENGTH)
    url = models.URLField()

    class Meta:
        db_table = "project_investment_social_links"

    def __str__(self) -> str:
        return f"{self.investment.organization_name} {self.platform}"

    @classmethod
    def get_permission_key(cls) -> str:
        return "project_investment_social_link"
