from autoslug import AutoSlugField
from django.db import models
from domain.constants import CHAR_FIELD_MAX_LENGTH, CHAR_FIELD_MEDIUM_LENGTH
from domain.models.base import BaseModel


class Company(BaseModel):
    name = models.CharField(max_length=CHAR_FIELD_MAX_LENGTH, unique=True)
    slug = AutoSlugField(populate_from="name", unique=True, max_length=CHAR_FIELD_MAX_LENGTH)
    description = models.TextField()
    country = models.ForeignKey("domain.Country", on_delete=models.PROTECT)
    business_id = models.CharField(max_length=32, unique=True)

    business_plan = models.FileField(upload_to="business_plans/", blank=True, null=True)
    established_date = models.DateField(blank=True, null=True)

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"

    def __str__(self) -> str:
        return self.name


class CompanyAttribute(BaseModel):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="attributes")
    key = models.CharField(max_length=CHAR_FIELD_MEDIUM_LENGTH)
    value = models.TextField()

    class Meta:
        unique_together = ("company", "key")

    def __str__(self) -> str:
        return f"{self.company.name} {self.key}"
