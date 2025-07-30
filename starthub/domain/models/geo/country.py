from django.core.validators import RegexValidator
from django.db import models
from domain.constants import COUNTRY_CODE_LENGTH
from domain.models.base import BaseModel


class Country(BaseModel):
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
        names = {
            "US": "United States",
            "RU": "Russia",
            "KZ": "Kazakhstan",
        }
        return names.get(self.code, self.code)

    @classmethod
    def get_permission_key(cls) -> str:
        return "country"
