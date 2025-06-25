from django.db import models
from domain.constants import CHAR_FIELD_SHORT_LENGTH
from domain.enums.role import RoleEnum
from domain.models.base import BaseModel


class Role(BaseModel):
    name = models.CharField(max_length=CHAR_FIELD_SHORT_LENGTH, unique=True)
    permissions = models.ManyToManyField("domain.Permission", related_name="roles")

    def __str__(self) -> str:
        return self.name

    class Meta:
        db_table = "roles"

    @classmethod
    def get_permission_key(cls) -> str:
        return "role"


def get_default_role() -> Role:
    role, _ = Role.objects.get_or_create(name=RoleEnum.get_default())
    return role
