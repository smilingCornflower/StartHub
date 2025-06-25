from datetime import UTC, datetime
from typing import Any

from django.db import models
from domain.constants import CHAR_FIELD_MAX_LENGTH
from domain.models.base import BaseModel


def get_default_datetime_now() -> datetime:
    return datetime.now(tz=UTC)


class News(BaseModel):
    title = models.CharField(max_length=CHAR_FIELD_MAX_LENGTH)
    image = models.CharField(max_length=CHAR_FIELD_MAX_LENGTH)
    content = models.TextField()
    author = models.ForeignKey("domain.User", on_delete=models.CASCADE)
    published_at = models.DateTimeField(default=get_default_datetime_now)
    updated_at = models.DateTimeField(default=get_default_datetime_now)

    class Meta:
        db_table = "news"

    def save(self, *args: Any, **kwargs: Any) -> None:
        self.updated_at = datetime.now(tz=UTC)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title

    @classmethod
    def get_permission_key(cls) -> str:
        return "news"
