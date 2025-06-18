from django.db import models
from domain.constants import CHAR_FIELD_SHORT_LENGTH
from domain.models.base import BaseModel


class Permission(BaseModel):
    name = models.CharField(max_length=CHAR_FIELD_SHORT_LENGTH, unique=True)
    description = models.TextField()

    def __str__(self) -> str:
        return self.name

    class Meta:
        db_table = "permissions"

    @classmethod
    def get_permission_key(cls) -> str:
        return "permission"
