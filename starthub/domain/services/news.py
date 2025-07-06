import re
import uuid
from pathlib import Path
from typing import Iterable

from domain.exceptions.validation import MissingFileExcpetion
from domain.models.news import News, NewsImage
from domain.ports.service import AbstractDomainService
from domain.repositories.news import (
    NewsImageReadRepository,
    NewsImageWriteRepository,
    NewsReadRepository,
    NewsWriteRepository,
)
from domain.value_objects.common import Id, Pagination
from domain.value_objects.file import Image
from domain.value_objects.filter import NewsFilter, NewsImageFilter
from domain.value_objects.news import (
    NewsContent,
    NewsCreatePayload,
    NewsImageCreatePayload,
    NewsImageDeletePayload,
    NewsUpdatePayload,
)
from loguru import logger


class NewsService(AbstractDomainService):
    IMAGES_PATTERN = re.compile(r"!\[(.*?)\]\((.*?)\)")

    def __init__(
        self,
        news_read_repository: NewsReadRepository,
        news_write_repository: NewsWriteRepository,
    ):
        self._news_read_repository = news_read_repository
        self._news_write_repository = news_write_repository

    def get_one(self, id_: Id) -> News:
        return self._news_read_repository.get_by_id(id_=id_)

    def get_many(self, filter_: NewsFilter, pagination: Pagination) -> list[News]:
        news: list[News] = self._news_read_repository.get_all(filter_=filter_, pagination=pagination)
        logger.debug(f"Found {len(news)} news")
        return news

    def create(self, payload: NewsCreatePayload) -> News:
        news: News = self._news_write_repository.create(data=payload)
        logger.info(f"News posted successfully with id = {news.id}")
        return news

    def replace_filenames_with_id(self, md: str, filenames: Iterable[str] | None = None) -> tuple[str, dict[str, str]]:
        """
        Replaces image filenames in Markdown content with UUIDs and builds a mapping of original to new names.

        Purpose:
            - Ensure unique image filenames by replacing original names with UUID-based names.
            - Produce a mapping {original_filename: new_filename} to later associate uploaded files correctly.

        How it works:
            - Searches for all Markdown image patterns: ![alt](filename)
            - If `filenames` is None:
                - Replaces all image filenames found in the Markdown
            - If `filenames` is a list:
                - Only replaces image filenames that are listed in `filenames`
            - For each replaced filename:
                - Generates a new UUID-based name (with ".jpg" extension)
                - Replaces the original filename in the Markdown string with the new name
            - Returns:
                - The updated Markdown content
                - A dictionary mapping original names to UUID-based names

        Example:
            Input:
                md = '![cat](cat.png) and ![dog](dog.jpg)'
                filenames = ['dog.jpg']
            Output:
                (
                    '![cat](cat.png) and ![dog](e7c3b57a-c7f7-4a02-8ef7-47d70a9de8a1.jpg)',
                    {'dog.jpg': 'e7c3b57a-c7f7-4a02-8ef7-47d70a9de8a1.jpg'}
                )
        """
        logger.debug(f"{filenames=}")

        uuid_map: dict[str, str] = {}
        new_md = md

        for matched in self.IMAGES_PATTERN.finditer(md):
            placeholder = matched.group(1)
            original_name = matched.group(2)
            if filenames is None or original_name in filenames:
                new_name = str(uuid.uuid4()) + ".jpg"
                uuid_map[original_name] = new_name
                new_md = new_md.replace(f"![{placeholder}]({original_name})", f"![{placeholder}]({new_name})", 1)
        return new_md, uuid_map

    def get_images_amount_in_content(self, content: NewsContent) -> int:
        count: int = len(self.IMAGES_PATTERN.findall(content.value))
        logger.debug(f"images count = {count}")
        return count

    def get_all_image_names_from_content(self, content: NewsContent) -> list[str]:
        result = list()
        for mathed in self.IMAGES_PATTERN.finditer(content.value):
            result.append(mathed.group(2))
        return result

    @staticmethod
    def check_image_presence(images_in_content: Iterable[str], images_in_files: Iterable[Image]) -> None:
        """:raises MissingFileExcpetion:"""
        for img in images_in_content:
            if img not in [i.name for i in images_in_files]:
                raise MissingFileExcpetion(f"Image {img} not provided in files.")

    def update(self, payload: NewsUpdatePayload) -> None:
        self._news_write_repository.update(data=payload)

    def delete_by_id(self, id_: Id) -> None:
        self._news_write_repository.delete_by_id(id_=id_)
        logger.debug("Deleted successfully")


class NewsImageService(AbstractDomainService):
    def __init__(
        self,
        news_image_read_repository: NewsImageReadRepository,
        news_image_write_repository: NewsImageWriteRepository,
    ):
        self._news_image_read_repository = news_image_read_repository
        self._news_image_write_repository = news_image_write_repository

    def create(self, data: NewsImageCreatePayload) -> NewsImage:
        return self._news_image_write_repository.create(data=data)

    def get(self, filter_: NewsImageFilter) -> list[NewsImage]:
        return self._news_image_read_repository.get_all(filter_=filter_)

    def delete(self, data: NewsImageDeletePayload) -> None:
        self._news_image_write_repository.delete(data=data)

    def extract_image_name(self, news_image: NewsImage) -> str:
        return Path(news_image.image).name
