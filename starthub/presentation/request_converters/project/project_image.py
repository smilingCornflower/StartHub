from django.core.files.uploadedfile import UploadedFile
from loguru import logger

from domain.value_objects.common import Id
from domain.value_objects.file import ImageFile
from domain.value_objects.project.image import ProjectImageCreateCommand
from presentation.request_converters.common import get_required_field


def request_files_to_project_image_create_command(
    files: dict[str, UploadedFile],
    project_id: int,
    user_id: int,
) -> ProjectImageCreateCommand:
    project_image_file: UploadedFile = get_required_field(files, "project_image")
    project_image_file.seek(0)
    image = ImageFile(value=project_image_file.read())
    logger.debug("request.FILES -> ImageFile conversion OK")
    project_image_create = ProjectImageCreateCommand(
        user_id=Id(value=user_id), project_id=Id(value=project_id), image_file=image
    )
    logger.debug("ProjectImageCreateCommand converted")
    return project_image_create
