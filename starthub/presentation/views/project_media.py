import pydantic
from application.services.gateway import gateway
from domain.exceptions import CustomException
from domain.value_objects.common import Id
from domain.value_objects.project.media import ProjectMediaCreateCommand
from infrastructure.auth.user import get_user_id_or_raises
from presentation.constants import SUCCESS
from presentation.request_converters.project.media import request_to_project_media_create_command
from presentation.response_factories.common import ProjectMediaErrorResponseFactory
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class ProjectMediaView(APIView):
    def post(self, request: Request, project_id: int) -> Response:
        try:
            user_id: Id = get_user_id_or_raises(request=request)
            command: ProjectMediaCreateCommand = request_to_project_media_create_command(request=request)
            gateway.project_media_app_service.create(user_id=user_id, project_id=Id(value=project_id), command=command)
            return Response({"code": SUCCESS}, status=status.HTTP_201_CREATED)

        except (CustomException, pydantic.ValidationError) as e:
            return ProjectMediaErrorResponseFactory.create_response(exception=e)
