from typing import Any

from application.converters.request_converters.common import get_required_field
from django.core.files.uploadedfile import UploadedFile
from domain.value_objects.common import Id
from domain.value_objects.file import ImageFile
from domain.value_objects.news import NewsContent, NewsCreateCommand, NewsTitle
from loguru import logger


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
