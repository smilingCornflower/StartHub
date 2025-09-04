import pydantic
from application.services.gateway import gateway
from domain.exceptions import CustomException
from domain.value_objects.common import Id
from domain.value_objects.project.media import ProjectMediaCreateCommand, ProjectMediaId, ProjectMediaUpdateCommand
from loguru import logger
from presentation.constants import SUCCESS
from presentation.helpers.auth import get_authenticated_user_from_request
from presentation.request_converters.project.media import (
    request_to_project_media_create_command,
    request_to_project_media_to_update_command,
)
from presentation.response_factories.project_management import ProjectMediaErrorResponseFactory
from pydantic import ValidationError
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class ProjectMediaView(APIView):
    def post(self, request: Request, project_id: int) -> Response:
        print()
        logger.info("POST /projects/media/")

        try:
            user = get_authenticated_user_from_request(request=request)
            user_id = Id(value=user.id)
            command: ProjectMediaCreateCommand = request_to_project_media_create_command(request=request)
            gateway.project_media_app_service.create(user_id=user_id, project_id=Id(value=project_id), command=command)
            return Response({"code": SUCCESS}, status=status.HTTP_201_CREATED)

        except (CustomException, pydantic.ValidationError) as e:
            return ProjectMediaErrorResponseFactory.create_response(exception=e)

    def patch(self, request: Request, project_id: int) -> Response:
        print()
        logger.info(f"PATCH /projects/{project_id}/media/")

        try:
            user = get_authenticated_user_from_request(request=request)
            user_id = Id(value=user.id)
            command: ProjectMediaUpdateCommand = request_to_project_media_to_update_command(request=request)
            gateway.project_media_app_service.update(user_id=user_id, project_id=Id(value=project_id), command=command)
            return Response({"code": SUCCESS}, status=status.HTTP_200_OK)

        except (CustomException, ValidationError) as e:
            return ProjectMediaErrorResponseFactory.create_response(exception=e)

    def delete(self, request: Request, project_media_id: int) -> Response:
        print()
        logger.info(f"DELETE /projects/media/{project_media_id}/")

        try:
            user = get_authenticated_user_from_request(request=request)
            user_id = Id(value=user.id)
            gateway.project_media_app_service.delete(
                user_id=user_id, project_media_id=ProjectMediaId(value=project_media_id)
            )
            return Response({"code": SUCCESS}, status=status.HTTP_201_CREATED)
        except (CustomException, pydantic.ValidationError) as e:
            return ProjectMediaErrorResponseFactory.create_response(exception=e)
