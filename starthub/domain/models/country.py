from django.db import models
from domain.constants import CHAR_FIELD_MEDIUM_LENGTH, COUNTRY_CODE_LENGTH
from domain.models.base import BaseModel


class Country(BaseModel):
    code = models.CharField(max_length=COUNTRY_CODE_LENGTH, unique=True)
    name = models.CharField(max_length=CHAR_FIELD_MEDIUM_LENGTH, unique=True)

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"

    def __str__(self) -> str:
        return self.name
