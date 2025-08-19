from django.db import models
from django.db.models import Manager
from domain.constants import CHAR_FIELD_MEDIUM_LENGTH
from domain.models.base import BaseModel


class City(BaseModel):
    objects: Manager["City"]

    name = models.CharField(max_length=CHAR_FIELD_MEDIUM_LENGTH)
    region = models.ForeignKey("domain.Region", on_delete=models.RESTRICT, related_name="cities")

    class Meta:
        db_table = "cities"
        unique_together = ("name", "region")

    def __str__(self) -> str:
        return f"{self.name}, {self.region}"

    @classmethod
    def get_permission_key(cls) -> str:
        return "city"
