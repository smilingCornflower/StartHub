from django.core.files.uploadedfile import UploadedFile
from rest_framework.request import Request

from domain.value_objects.file import FileVo
from domain.value_objects.project.project_file import ProjectFileCreateCommand, ProjectFileName
from presentation.request_converters.common import get_required_field


def request_to_project_file_create_command(request: Request) -> ProjectFileCreateCommand:
    project_file: UploadedFile = get_required_field(request.FILES, "project_file")
    project_file.seek(0)

    return ProjectFileCreateCommand(
        file=FileVo(value=project_file.read()),
        name=ProjectFileName(value=project_file.name) if project_file.name else None,
    )
