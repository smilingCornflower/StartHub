from django.db import models

from domain.constants import CHAR_FIELD_MEDIUM_LENGTH
from domain.models.base import BaseModel


class Region(BaseModel):
    name = models.CharField(max_length=CHAR_FIELD_MEDIUM_LENGTH)
    country = models.ForeignKey("domain.Country", on_delete=models.RESTRICT, related_name="regions")

    class Meta:
        unique_together = ('name', 'country')

    def __str__(self) -> str:
        return f"{self.name}, {self.country}"

    @classmethod
    def get_permission_key(cls) -> str:
        return "region"
