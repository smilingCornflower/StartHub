from django.db import models
from domain.constants import CHAR_FIELD_MAX_LENGTH, CHAR_FIELD_MEDIUM_LENGTH, CHAR_FIELD_SHORT_LENGTH
from domain.models.base import BaseModel

POSTAL_CODE_LENGTH = 20


class Address(BaseModel):
    country = models.ForeignKey("domain.Country", on_delete=models.RESTRICT, related_name="addresses")
    region = models.ForeignKey("domain.Region", on_delete=models.RESTRICT, related_name="addresses")
    city = models.ForeignKey("domain.City", on_delete=models.RESTRICT, related_name="addresses")
    district = models.CharField(max_length=CHAR_FIELD_MEDIUM_LENGTH, blank=True, null=True)
    street = models.CharField(max_length=CHAR_FIELD_MEDIUM_LENGTH, blank=True, null=True)
    house_number = models.CharField(max_length=CHAR_FIELD_SHORT_LENGTH, blank=True, null=True)
    postal_code = models.CharField(max_length=POSTAL_CODE_LENGTH, blank=True, null=True)

    raw_address = models.CharField(max_length=CHAR_FIELD_MAX_LENGTH, blank=True, null=True)

    class Meta:
        db_table = "addresses"
        unique_together = (
            "country",
            "region",
            "city",
            "district",
            "street",
            "house_number",
            "postal_code",
            "raw_address",
        )

    def __str__(self) -> str:
        if self.raw_address:
            return self.raw_address

        parts = [
            str(self.country),
            str(self.region),
            str(self.city),
            self.district,
            self.street,
            self.house_number,
            self.postal_code,
        ]
        return ", ".join(filter(None, parts))

    @classmethod
    def get_permission_key(cls) -> str:
        return "address"
