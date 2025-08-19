from idlelib.query import Query

from django.db import models
from domain.constants import CHAR_FIELD_MEDIUM_LENGTH
from domain.models.base import BaseModel
from django.db.models import Manager, QuerySet


from domain.models.geo.country import Country
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from domain.models.geo.city import City

class Region(BaseModel):  # type: ignore[django-manager-missing]
    objects: Manager["Region"]

    name = models.CharField(max_length=CHAR_FIELD_MEDIUM_LENGTH)
    country = models.ForeignKey(Country, on_delete=models.RESTRICT, related_name="regions")

    class Meta:
        db_table = "regions"
        unique_together = ("name", "country")

    def __str__(self) -> str:
        return f"{self.name}, {self.country}"

    @classmethod
    def get_permission_key(cls) -> str:
        return "region"
