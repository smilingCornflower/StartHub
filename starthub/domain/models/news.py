from datetime import UTC, datetime
from typing import Any

from django.db import models
from domain.constants import CHAR_FIELD_MAX_LENGTH
from domain.models.base import BaseModel


def get_default_datetime_now() -> datetime:
    return datetime.now(tz=UTC)


class News(BaseModel):
    title = models.CharField(max_length=CHAR_FIELD_MAX_LENGTH)
    subtitle = models.TextField(null=True)
    content = models.TextField()
    author = models.ForeignKey("domain.User", on_delete=models.CASCADE)
    published_at = models.DateTimeField(default=get_default_datetime_now)
    updated_at = models.DateTimeField(default=get_default_datetime_now)
    cover = models.CharField(max_length=CHAR_FIELD_MAX_LENGTH, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    IS_ACTIVE_FIELD = "is_active"

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


class NewsImage(BaseModel):
    news = models.ForeignKey("domain.News", on_delete=models.CASCADE, related_name="images")
    image = models.CharField(max_length=CHAR_FIELD_MAX_LENGTH)

    class Meta:
        db_table = "news_images"

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(news={self.news}, image={self.image})"

    @classmethod
    def get_permission_key(cls) -> str:
        return "news_images"
