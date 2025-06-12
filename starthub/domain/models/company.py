from autoslug import AutoSlugField
from django.db import models
from domain.constants import CHAR_FIELD_MAX_LENGTH, CHAR_FIELD_SHORT_LENGTH
from domain.models.base import BaseModel


class CompanyFounder(BaseModel):
    name = models.CharField(max_length=CHAR_FIELD_SHORT_LENGTH)
    surname = models.CharField(max_length=CHAR_FIELD_SHORT_LENGTH)
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "company_founder"

    def __str__(self) -> str:
        return f"{self.name} {self.surname}"


class Company(BaseModel):
    name = models.CharField(max_length=CHAR_FIELD_MAX_LENGTH)
    slug = AutoSlugField(populate_from="name", unique=True, max_length=CHAR_FIELD_MAX_LENGTH)
    founder = models.OneToOneField("domain.CompanyFounder", on_delete=models.PROTECT, related_name="company")
    representative = models.ForeignKey("domain.User", on_delete=models.PROTECT, related_name="companies")

    description = models.TextField()
    country = models.ForeignKey("domain.Country", on_delete=models.PROTECT)
    business_id = models.CharField(max_length=32, unique=True)

    business_plan = models.FileField(upload_to="business_plans/", blank=True, null=True)
    established_date = models.DateField()

    class Meta:
        db_table = "company"
        verbose_name = "Company"
        verbose_name_plural = "Companies"

    def __str__(self) -> str:
        return self.name
