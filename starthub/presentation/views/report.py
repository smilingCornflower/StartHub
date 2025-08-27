from dataclasses import asdict

from application.services.gateway import gateway
from domain.exceptions import CustomException
from domain.value_objects.common import Id
from infrastructure.auth.user import get_user_id_or_raises
from loguru import logger
from presentation.request_converters.common import request_to_cursor_pagination
from presentation.response_factories.report import ProjectReportErrorResponseFactory
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class ProjectReportView(APIView):
    @staticmethod
    def get(request: Request, project_id: int) -> Response:
        print()
        logger.info(f"GET /projects/{project_id}/reports/")

        try:
            user_id: Id = get_user_id_or_raises(request=request)
            pagination = request_to_cursor_pagination(request=request)
            reports = gateway.project_report_app_service.get_reports_to_project(
                user_id=user_id,
                project_id=Id(value=project_id),
                pagination=pagination,
            )
            return Response(list(map(asdict, reports)), status=status.HTTP_200_OK)
        except CustomException as e:
            return ProjectReportErrorResponseFactory.create_response(exception=e)
