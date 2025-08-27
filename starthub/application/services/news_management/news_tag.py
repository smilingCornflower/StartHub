from application.ports.service import AbstractAppService
from domain.enums.news_tag import NewsTagEnum
from domain.exceptions.validation import ValidationException
from domain.repositories.news_management.news import NewsReadRepository
from domain.repositories.user_management.user import UserReadRepository
from domain.services.news_management.news_tag import NewsTagService
from domain.value_objects.common import Id
from loguru import logger


class NewsTagAppService(AbstractAppService):
    def __init__(
        self,
        news_tag_service: NewsTagService,
        user_read_repository: UserReadRepository,
        news_read_repository: NewsReadRepository,
    ):
        self._news_tag_service = news_tag_service
        self._user_read_repository = user_read_repository
        self._news_read_repository = news_read_repository

    def _get_tag_name_enum(self, tag_name: str) -> NewsTagEnum:
        """:raises ValidationException:"""
        try:
            return NewsTagEnum(tag_name)
        except ValueError:
            raise ValidationException(f"Invalid value for tag: {tag_name}.")

    def delete_tag_from_news(self, user_id: Id, news_id: Id, tag_name: str) -> None:
        user = self._user_read_repository.get_by_id(id_=user_id)
        news = self._news_read_repository.get_by_id(id_=news_id)
        tag_name_enum = self._get_tag_name_enum(tag_name=tag_name)

        self._news_tag_service.delete_tag_from_news(user=user, news=news, tag_name=tag_name_enum)
        logger.info(f"Tag {tag_name} was deleted from the News(id={news.id}) successfully ")

    def add_tag_to_news(self, user_id: Id, news_id: Id, tag_name: NewsTagEnum) -> None:
        user = self._user_read_repository.get_by_id(id_=user_id)
        news = self._news_read_repository.get_by_id(id_=news_id)

        self._news_tag_service.add_tag_to_news(user=user, news=news, tag_name=tag_name)
        logger.info(f"Tag {tag_name} was added to the News(id={news.id}) successfully ")
