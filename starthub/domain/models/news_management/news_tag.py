from django.db import models
from domain.constants import CHAR_FIELD_SHORT_LENGTH
from domain.models.base import BaseModel

NEWS_TAG_NAME_LENGTH = CHAR_FIELD_SHORT_LENGTH


class NewsTagsLink(BaseModel):
    news = models.ForeignKey("domain.News", on_delete=models.CASCADE)
    tag = models.ForeignKey("domain.NewsTag", on_delete=models.CASCADE)

    class Meta:
        db_table = "news_tags_links"
        unique_together = ("news", "tag")

    def __str__(self) -> str:
        return f"({self.news.title}, {self.tag.name})"

    @classmethod
    def get_permission_key(cls) -> str:
        return "news_tags_links"


class NewsTag(BaseModel):
    name = models.CharField(max_length=NEWS_TAG_NAME_LENGTH, unique=True)

    class Meta:
        db_table = "news_tags"

    def __str__(self) -> str:
        return str(self.name)

    @classmethod
    def get_permission_key(cls) -> str:
        return "news_tag"
