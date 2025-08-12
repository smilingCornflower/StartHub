from application.services.gateway import gateway
from domain.exceptions import CustomException
from domain.value_objects.common import Id
from domain.value_objects.project.government_grant import (
    ProjectGovernmentGrantCreateCommand,
    ProjectGovernmentGrantId,
    ProjectGoverntmentGrantUpdateCommand,
)
from infrastructure.auth.user import get_user_id_or_raises
from loguru import logger
from presentation.constants import SUCCESS
from presentation.request_converters.project.government_grant import (
    request_to_project_government_grant_create_command,
    request_to_project_government_grant_update_command,
)
from presentation.response_factories.common import ProjectGovernmentGrantErrorResponseFactory
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class GovernmentGrantView(APIView):
    def post(self, request: Request, project_id: int) -> Response:
        print()
        logger.info(f"GovermentGrant POST, {project_id=}")
        try:
            user_id: Id = get_user_id_or_raises(request=request)
            command: ProjectGovernmentGrantCreateCommand = request_to_project_government_grant_create_command(
                request=request
            )
            gateway.project_government_grant_app_service.create(
                user_id=user_id, project_id=Id(value=project_id), command=command
            )

            return Response({"code": SUCCESS}, status=status.HTTP_201_CREATED)
        except CustomException as e:
            return ProjectGovernmentGrantErrorResponseFactory.create_response(exception=e)

    def patch(self, request: Request, government_grant_id: int) -> Response:
        print()
        logger.info(f"GovermentGrant PATCH, {government_grant_id=}")
        try:
            user_id: Id = get_user_id_or_raises(request=request)
            command: ProjectGoverntmentGrantUpdateCommand = request_to_project_government_grant_update_command(
                request=request
            )
            gateway.project_government_grant_app_service.update(
                user_id=user_id,
                government_grant_id=ProjectGovernmentGrantId(value=government_grant_id),
                command=command,
            )
            return Response({"code": SUCCESS}, status=status.HTTP_200_OK)
        except CustomException as e:
            return ProjectGovernmentGrantErrorResponseFactory.create_response(exception=e)

    def delete(self, request: Request, government_grant_id: int) -> Response:
        print()
        logger.info(f"GovernmentGrant DELETE, {government_grant_id=}")
        try:
            user_id: Id = get_user_id_or_raises(request=request)
            gateway.project_government_grant_app_service.delete(
                user_id=user_id, government_grant_id=ProjectGovernmentGrantId(value=government_grant_id)
            )

            return Response({"code": SUCCESS}, status=status.HTTP_200_OK)
        except CustomException as e:
            return ProjectGovernmentGrantErrorResponseFactory.create_response(exception=e)
