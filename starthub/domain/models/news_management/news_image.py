from django.db import models
from domain.constants import CHAR_FIELD_MAX_LENGTH
from domain.models.base import BaseModel


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
