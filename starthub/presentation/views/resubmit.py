from application.services.gateway import gateway
from domain.exceptions import CustomException
from domain.value_objects.common import Id
from infrastructure.auth.user import get_user_id_or_raises
from loguru import logger
from presentation.constants import SUCCESS
from presentation.response_factories.report import ProjectReportErrorResponseFactory
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class ProjectResubmitView(APIView):
    @staticmethod
    def patch(request: Request, project_id: int) -> Response:
        print()
        logger.info(f"POST /projects/{project_id}/resubmit/")

        try:
            user_id = get_user_id_or_raises(request=request)
            gateway.project_resubmit_app_service.resubmit(
                user_id=user_id,
                project_id=Id(value=project_id),
            )
            return Response({"code": SUCCESS}, status=status.HTTP_200_OK)
        except CustomException as e:
            return ProjectReportErrorResponseFactory.create_response(exception=e)
