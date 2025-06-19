from typing import Any

from application.converters.request_converters.news import request_to_news_create_command
from application.ports.service import AbstractAppService
from django.core.files.uploadedfile import UploadedFile
from domain.models.news import News
from domain.services.news import NewsService
from loguru import logger


class NewsAppService(AbstractAppService):
    def __init__(self, news_service: NewsService):
        self._news_service = news_service

    def create(self, request_data: dict[str, Any], request_files: dict[str, UploadedFile], user_id: int) -> News:
        news_create_command = request_to_news_create_command(
            request_data=request_data, request_files=request_files, user_id=user_id
        )
        logger.debug(f"command = {news_create_command}")
        news: News = self._news_service.create(news_create_command)
        logger.info("News created successfully.")
        return news
