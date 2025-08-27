from domain.enums.news_tag import NewsTagEnum
from domain.ports.payload import AbstractCreatePayload, AbstractUpdatePayload
from domain.value_objects.common import Id


class NewsTagId(Id):
    pass


class NewsTagCreatePayload(AbstractCreatePayload):
    name: NewsTagEnum


class NewsTagUpdatePayload(AbstractUpdatePayload):
    pass
