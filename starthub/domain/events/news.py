from domain.enums.event import EventType
from domain.enums.news_tag import NewsTagEnum
from domain.events.base import DomainEvent
from domain.value_objects.common import Id
from pydantic import Field


class NewsCreatedEvent(DomainEvent):
    news_id: Id
    tags: list[NewsTagEnum] | None

    event_type: EventType.News = Field(default=EventType.News.CREATED)
