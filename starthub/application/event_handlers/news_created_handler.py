from typing import cast

from domain.enums.news_tag import NewsTagEnum
from domain.events.news import NewsCreatedEvent
from domain.exceptions.news import NewsTagNotFoundException
from domain.models.news_management.news_tag import NewsTag
from domain.ports.event import AbstractEventHandler
from domain.repositories.news_management.news_tag import NewsTagReadRepository
from domain.repositories.news_management.news_tags_link import NewsTagsLinkWriteRepository
from domain.value_objects.common import Id
from domain.value_objects.filter import NewsTagFilter
from domain.value_objects.news_management.news_tags_link import NewsTagsLinkCreatePayload
from loguru import logger


class NewsCreatedEventHandler(AbstractEventHandler[NewsCreatedEvent]):
    def __init__(
        self,
        news_tag_read_repository: NewsTagReadRepository,
        news_tags_link_write_repository: NewsTagsLinkWriteRepository,
    ):
        self._news_tag_read_repository = news_tag_read_repository
        self._news_tags_link_write_repository = news_tags_link_write_repository

    def handle(self, event: NewsCreatedEvent) -> None:
        if event.tags:
            self.assign_tags(event.news_id, event.tags)

    def assign_tags(self, news_id: Id, tags: list[NewsTagEnum]) -> None:
        """:raises NewsTagNotFoundException:"""
        news_tags: list[NewsTag] = self._news_tag_read_repository.get_all(filter_=NewsTagFilter(tag_names=tags))

        if len(news_tags) < len(tags):
            missing_tags = cast(set[str], set(tags)) - set([i.name for i in news_tags])
            raise NewsTagNotFoundException(f"Tags not found: {', '.join(missing_tags)}")

        for tag in news_tags:
            create_payload = NewsTagsLinkCreatePayload(news_id=news_id, news_tag_id=Id(value=tag.id))
            self._news_tags_link_write_repository.create(data=create_payload)
            logger.debug("NewsTag(name={tag.name}) added.")

        logger.info("All tags added successfully.")
