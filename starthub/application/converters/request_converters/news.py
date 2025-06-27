from typing import Any

from django.core.files.uploadedfile import UploadedFile
from loguru import logger

from application.converters.request_converters.common import get_required_field
from domain.value_objects.common import Id
from domain.value_objects.file import ImageFile
from domain.value_objects.filter import NewsFilter
from domain.value_objects.news import NewsContent, NewsCreateCommand, NewsTitle, NewsUpdateCommand


def request_to_news_create_command(
    request_data: dict[str, Any], request_files: dict[str, UploadedFile], user_id: int
) -> NewsCreateCommand:
    project_image_file: UploadedFile = get_required_field(request_files, "project_image")
    project_image_file.seek(0)
    image = ImageFile(value=project_image_file.read())
    logger.debug("request.FILES -> ImageFile conversion OK")

    return NewsCreateCommand(
        title=NewsTitle(value=get_required_field(request_data, "title")),
        content=NewsContent(value=get_required_field(request_data, "content")),
        author_id=Id(value=user_id),
        image=image,
    )


def request_to_news_update_command(
    request_data: dict[str, Any], request_files: dict[str, UploadedFile], news_id: int, user_id: int
) -> NewsUpdateCommand:
    image: ImageFile | None = None
    if "image" in request_files:
        news_image: UploadedFile = request_files["image"]
        news_image.seek(0)
        image = ImageFile(value=news_image.read())
    return NewsUpdateCommand(
        news_id=Id(value=news_id),
        title=NewsTitle(value=request_data["title"]) if "title" in request_data else None,
        content=NewsContent(value=request_data["content"]) if "content" in request_data else None,
        image=image,
    )


def request_to_news_filter(request_data: dict[str, Any]) -> NewsFilter:
    return NewsFilter()
