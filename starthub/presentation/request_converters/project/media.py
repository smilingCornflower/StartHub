from django.core.files.uploadedfile import UploadedFile
from domain.value_objects.project.media import MediaFile, ProjectMediaCreateCommand
from presentation.request_converters.common import get_required_field
from rest_framework.request import Request


def request_to_project_media_create_command(request: Request) -> ProjectMediaCreateCommand:
    project_file: UploadedFile = get_required_field(request.FILES, "project_media")
    project_file.seek(0)

    return ProjectMediaCreateCommand(media=MediaFile(value=project_file.read()))
