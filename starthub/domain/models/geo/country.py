from django.core.validators import RegexValidator
from django.db import models
from domain.constants import COUNTRY_CODE_LENGTH
from domain.models.base import BaseModel
from django.db.models import Manager, QuerySet
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from domain.models.geo.region import Region

class Country(BaseModel):  # type: ignore[django-manager-missing]
    objects: Manager["Country"]

    code = models.CharField(
        max_length=COUNTRY_CODE_LENGTH,
        unique=True,
        validators=[RegexValidator(regex=r"^[A-Z]{2}$", message="Invalid country code")],
        verbose_name="Country code",
    )

    class Meta:
        db_table = "countries"
        verbose_name = "Country"
        verbose_name_plural = "Countries"

    def __str__(self) -> str:
        return self.code

    @classmethod
    def get_permission_key(cls) -> str:
        return "country"
