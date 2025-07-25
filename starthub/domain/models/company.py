from autoslug import AutoSlugField
from django.db import models
from domain.constants import CHAR_FIELD_MAX_LENGTH, CHAR_FIELD_SHORT_LENGTH
from domain.models.base import BaseModel


class CompanyFounder(BaseModel):
    name = models.CharField(max_length=CHAR_FIELD_SHORT_LENGTH)
    surname = models.CharField(max_length=CHAR_FIELD_SHORT_LENGTH)
    company = models.OneToOneField("domain.Company", on_delete=models.CASCADE, related_name="founder")
    description = models.TextField()

    class Meta:
        db_table = "company_founder"

    def __str__(self) -> str:
        return f"{self.name} {self.surname}"

    @classmethod
    def get_permission_key(cls) -> str:
        return "company_founder"


class Company(BaseModel):
    name = models.CharField(max_length=CHAR_FIELD_MAX_LENGTH)
    slug = AutoSlugField(populate_from="name", unique=True, max_length=CHAR_FIELD_MAX_LENGTH)
    project = models.OneToOneField("domain.Project", on_delete=models.CASCADE)
    country = models.ForeignKey("domain.Country", on_delete=models.PROTECT)
    business_id = models.CharField(max_length=32, unique=True)
    established_date = models.DateField()

    class Meta:
        db_table = "company"
        verbose_name = "Company"
        verbose_name_plural = "Companies"

    def __str__(self) -> str:
        return self.name

    @classmethod
    def get_permission_key(cls) -> str:
        return "company"
