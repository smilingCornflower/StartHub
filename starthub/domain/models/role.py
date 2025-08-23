from typing import Any, Callable

from django.db import models
from domain.constants import CHAR_FIELD_SHORT_LENGTH
from domain.enums.role import RoleEnum
from domain.models.base import BaseModel
from pydantic_core import core_schema


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

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: type[Any], handler: Callable[[type[Any]], core_schema.CoreSchema]
    ) -> core_schema.CoreSchema:
        return core_schema.model_schema(
            cls,
            core_schema.model_fields_schema(
                {
                    "id": core_schema.model_field(core_schema.int_schema()),
                    "name": core_schema.model_field(core_schema.str_schema()),
                }
            ),
        )


def get_default_role() -> Role:
    role, _ = Role.objects.get_or_create(name=RoleEnum.get_default())
    return role
