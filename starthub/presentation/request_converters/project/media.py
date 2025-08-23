from django.core.files.uploadedfile import UploadedFile
from rest_framework.request import Request

from domain.value_objects.common import Order
from domain.value_objects.project.media import MediaFile, ProjectMediaCreateCommand, ProjectMediaUpdateCommand
from presentation.request_converters.common import get_required_field


def request_to_project_media_create_command(request: Request) -> ProjectMediaCreateCommand:
    project_file: UploadedFile = get_required_field(request.FILES, "project_media")
    project_file.seek(0)

    return ProjectMediaCreateCommand(media=MediaFile(value=project_file.read()))


def request_to_project_media_to_update_command(request: Request) -> ProjectMediaUpdateCommand:
    data = request.data
    new_order: list[Order] | None = None
    if "new_order" in data:
        new_order = [Order(value=i) for i in data["new_order"]]

    return ProjectMediaUpdateCommand(new_order=new_order)
