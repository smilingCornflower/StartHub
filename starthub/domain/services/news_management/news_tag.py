from domain.enums.news_tag import NewsTagEnum
from domain.enums.permission import ActionEnum, ScopeEnum
from domain.exceptions.permissions import UpdateDeniedPermissionException
from domain.models.news_management.news import News
from domain.models.user_management.user import User
from domain.ports.service import AbstractDomainService
from domain.repositories.news_management.news_tag import NewsTagReadRepository
from domain.repositories.news_management.news_tags_link import NewsTagsLinkWriteRepository
from domain.services.permission import PermissionService
from domain.value_objects.common import Id
from domain.value_objects.news_management.news_tags_link import NewsTagsLinkCreatePayload


class NewsTagPermissionService(AbstractDomainService):
    def __init__(self, permission_service: PermissionService):
        self._permission_service = permission_service

    def _check_permission_to_change_news(self, user: User) -> None:
        """:raises UpdateDeniedPermissionException:"""
        if self._permission_service.is_allowed_for_user(
            user=user,
            model=News,
            action=ActionEnum.CHANGE,
            scope=ScopeEnum.ANY,
        ):
            return None
        raise UpdateDeniedPermissionException("You don't have enough permissions to update news.")


class NewsTagService(NewsTagPermissionService):
    def __init__(
        self,
        permission_service: PermissionService,
        news_tag_read_repository: NewsTagReadRepository,
        news_tags_link_write_repository: NewsTagsLinkWriteRepository,
    ):
        super().__init__(permission_service=permission_service)
        self._news_tag_read_repository = news_tag_read_repository
        self._news_tags_link_write_repository = news_tags_link_write_repository

    def add_tag_to_news(self, user: User, news: News, tag_name: NewsTagEnum) -> None:
        self._check_permission_to_change_news(user=user)

        news_tag = self._news_tag_read_repository.get_by_name(name=tag_name)
        self._news_tags_link_write_repository.get_or_create(
            data=NewsTagsLinkCreatePayload(news_id=Id(value=news.id), news_tag_id=Id(value=news_tag.id)),
        )

    def delete_tag_from_news(self, user: User, news: News, tag_name: NewsTagEnum) -> None:
        self._check_permission_to_change_news(user=user)

        news_tag = self._news_tag_read_repository.get_by_name(name=tag_name)
        self._news_tags_link_write_repository.delete_by_association_ids(
            news_id=Id(value=news.id), tag_id=Id(value=news_tag.id)
        )
