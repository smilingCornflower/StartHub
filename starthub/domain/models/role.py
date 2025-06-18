from domain.constants import CHAR_FIELD_SHORT_LENGTH
from domain.models.base import BaseModel
from django.db import models
from domain.enums.role import RoleEnum


class Role(BaseModel):
    name = models.CharField(max_length=CHAR_FIELD_SHORT_LENGTH, unique=True)
    permissions = models.ManyToManyField

    def __str__(self) -> str:
        return self.name

    class Meta:
        db_table = "roles"


def get_default_role() -> Role:
    role, _ = Role.objects.get_or_create(name=RoleEnum.get_default())
    return role
