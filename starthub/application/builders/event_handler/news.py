from typing import Any

from application.event_handlers.news_created_handler import NewsCreatedEventHandler
from application.ports.event_handler_builder import AbstractEventHandlerBuilder
from infrastructure.repositories.news_management.news_tag import DjNewsTagReadRepository
from infrastructure.repositories.news_management.news_tags_link import DjNewsTagsLinkWriteRepository


class NewsCreatedEventHandlerBuilder(AbstractEventHandlerBuilder[Any]):
    @staticmethod
    def create_handler() -> NewsCreatedEventHandler:
        return NewsCreatedEventHandler(
            news_tag_read_repository=DjNewsTagReadRepository(),
            news_tags_link_write_repository=DjNewsTagsLinkWriteRepository(),
        )
