import pydantic
from application.services.gateway import gateway
from domain.exceptions import CustomException
from domain.value_objects.project.stage import ProjectStageId
from infrastructure.auth.user import get_user_id_or_raises
from loguru import logger
from presentation.constants import SUCCESS
from presentation.request_converters.project.stage import request_to_project_stage_update_command
from presentation.response_factories.project_management import ProjectStageErrorResponseFactory
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class ProjectStageView(APIView):
    @staticmethod
    def patch(request: Request, stage_id: int) -> Response:
        print()
        logger.info(f"{request.method}, {request.path}")
        try:
            user_id = get_user_id_or_raises(request=request)
            command = request_to_project_stage_update_command(request=request)
            gateway.project_stage_app_service.update(
                user_id=user_id,
                stage_id=ProjectStageId(value=stage_id),
                command=command,
            )
            return Response({"code": SUCCESS}, status=status.HTTP_200_OK)
        except (CustomException, pydantic.ValidationError) as e:
            return ProjectStageErrorResponseFactory.create_response(exception=e)
