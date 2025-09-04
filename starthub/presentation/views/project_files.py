from application.services.gateway import gateway
from domain.exceptions import CustomException
from domain.value_objects.common import Id
from domain.value_objects.project.project_file import ProjectFileCreateCommand, ProjectFileId
from presentation.constants import SUCCESS
from presentation.helpers.auth import get_authenticated_user_from_request
from presentation.request_converters.project.project_file import request_to_project_file_create_command
from presentation.response_factories.project_management import ProjectFileErrorResponseFactory
from pydantic import ValidationError
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class ProjectFileView(APIView):
    def post(self, request: Request, project_id: int) -> Response:
        try:
            user = get_authenticated_user_from_request(request=request)
            user_id = Id(value=user.id)
            command: ProjectFileCreateCommand = request_to_project_file_create_command(request=request)
            gateway.project_file_app_service.create(user_id=user_id, project_id=Id(value=project_id), command=command)
            return Response({"code": SUCCESS}, status=status.HTTP_201_CREATED)
        except (CustomException, ValidationError) as e:
            return ProjectFileErrorResponseFactory.create_response(exception=e)

    def delete(self, request: Request, project_file_id: int) -> Response:
        try:
            user = get_authenticated_user_from_request(request=request)
            user_id = Id(value=user.id)
            gateway.project_file_app_service.delete(
                user_id=user_id, project_file_id=ProjectFileId(value=project_file_id)
            )
            return Response({"code": SUCCESS}, status=status.HTTP_201_CREATED)
        except (CustomException, ValidationError) as e:
            return ProjectFileErrorResponseFactory.create_response(exception=e)
