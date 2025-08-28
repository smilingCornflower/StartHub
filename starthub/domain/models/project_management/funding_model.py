from autoslug import AutoSlugField
from django.db import models
from domain.constants import CHAR_FIELD_SHORT_LENGTH, DESCRIPTION_MAX_LENGTH
from domain.models.base import BaseModel


class FundingModel(BaseModel):
    name = models.CharField(max_length=CHAR_FIELD_SHORT_LENGTH, unique=True)
    slug = AutoSlugField(populate_from="name", unique=True, max_length=CHAR_FIELD_SHORT_LENGTH)
    description = models.CharField(max_length=DESCRIPTION_MAX_LENGTH, null=True)
    recommended = models.BooleanField(default=False)

    class Meta:
        db_table = "funding_models"
        verbose_name = "Funding Model"
        verbose_name_plural = "Funding Models"

    def __str__(self) -> str:
        return self.name

    @classmethod
    def get_permission_key(cls) -> str:
        return "funding_model"
