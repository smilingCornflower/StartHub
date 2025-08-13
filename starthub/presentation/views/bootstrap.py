from application.services.gateway import gateway
from domain.exceptions import CustomException
from domain.value_objects.common import Id
from domain.value_objects.project.bootstrap import (
    ProjectBootstrapCreateCommand,
    ProjectBootstrapId,
    ProjectBootstrapUpdateCommand,
)
from infrastructure.auth.user import get_user_id_or_raises
from loguru import logger
from presentation.constants import SUCCESS
from presentation.request_converters.project.bootstrap import (
    request_to_project_bootstrap_create_command,
    request_to_project_bootstrap_update_command,
)
from presentation.response_factories.common import ProjectBootstrapErrorResponseFactory
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class ProjectBootstrapView(APIView):
    def post(self, request: Request, project_id: int) -> Response:
        logger.info(f"POST /projects/{project_id}/bootstraps/")
        try:
            user_id: Id = get_user_id_or_raises(request=request)
            command: ProjectBootstrapCreateCommand = request_to_project_bootstrap_create_command(request=request)
            gateway.project_bootstrap_app_service.create(
                user_id=user_id, project_id=Id(value=project_id), command=command
            )
            return Response({"code": SUCCESS}, status=status.HTTP_200_OK)
        except CustomException as e:
            return ProjectBootstrapErrorResponseFactory.create_response(exception=e)

    def patch(self, request: Request, bootstrap_id: int) -> Response:
        logger.info(f"PATCH /projects/bootstraps/{bootstrap_id}/")
        try:
            user_id: Id = get_user_id_or_raises(request=request)
            command: ProjectBootstrapUpdateCommand = request_to_project_bootstrap_update_command(request=request)
            gateway.project_bootstrap_app_service.update(
                user_id=user_id, bootstrap_id=ProjectBootstrapId(value=bootstrap_id), command=command
            )
            return Response({"code": SUCCESS}, status=status.HTTP_200_OK)
        except CustomException as e:
            return ProjectBootstrapErrorResponseFactory.create_response(exception=e)
