from typing import Any

from django.core.files.uploadedfile import UploadedFile
from loguru import logger

from application.converters.request_converters.news import request_to_news_create_command, request_to_news_filter
from application.converters.resposne_converters.news import news_to_dto
from application.dto.news import NewsDto
from application.ports.service import AbstractAppService
from domain.enums.permission import ActionEnum, ScopeEnum
from domain.exceptions.permissions import AddDeniedPermissionException
from domain.models.news import News
from domain.services.news import NewsService
from domain.services.permission import PermissionService
from domain.value_objects.common import Id
from domain.value_objects.filter import NewsFilter
from domain.value_objects.news import NewsCreateCommand
from domain.value_objects.user import PermissionVo

from pprint import pformat


class NewsAppService(AbstractAppService):
    def __init__(self, news_service: NewsService, permission_service: PermissionService):
        self._news_service = news_service
        self._permission_service = permission_service

    def get(self, request_data: dict[str, Any], news_id: int | None = None) -> list[NewsDto]:
        if news_id:
            news: News = self._news_service.get_one(Id(value=news_id))
            news_dto: NewsDto = news_to_dto(news)
            return [news_dto]
        else:
            news_filter: NewsFilter = request_to_news_filter(request_data=request_data)
            news: list[News] = self._news_service.get_many(filter_=news_filter)
            return [news_to_dto(i) for i in news]

    def create(self, request_data: dict[str, Any], request_files: dict[str, UploadedFile], user_id: int) -> News:
        news_create_command: NewsCreateCommand = request_to_news_create_command(
            request_data=request_data, request_files=request_files, user_id=user_id
        )
        logger.debug(f"news_create_command = {pformat(news_create_command)}")

        add_news_permission: PermissionVo = self._permission_service.create_permission_vo(
            model=News, action=ActionEnum.ADD, scope=ScopeEnum.ANY
        )
        has_permission: bool = self._permission_service.has_permission(
            user_id=Id(value=user_id), permission_vo=add_news_permission
        )
        logger.debug(f"user_id = {user_id}; has_permission = {has_permission}")
        if has_permission:
            logger.debug(f"command = {news_create_command}")
            news: News = self._news_service.create(news_create_command)
            logger.info("News created successfully.")
            return news
        else:
            logger.exception("User does not have permission to add news")
            raise AddDeniedPermissionException("User does not have permission to add news")
