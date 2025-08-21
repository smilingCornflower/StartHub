import pydantic
from application.services.gateway import gateway
from domain.exceptions import CustomException
from domain.value_objects.common import Id
from infrastructure.auth.user import get_user_id_or_raises
from loguru import logger
from presentation.constants import SUCCESS
from presentation.response_factories.admin import ProjectSubmissionErrorResponseFactory
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class ProjectSubmissionApproveView(APIView):
    @staticmethod
    def patch(request: Request, project_id: int) -> Response:
        print()
        logger.warning(f"PATCH /admin/project-submissions/{project_id}/approve/")
        try:
            user_id: Id = get_user_id_or_raises(request=request)
            gateway.project_submission_app_service.approve(user_id=user_id, project_id=Id(value=project_id))
            return Response({"code": SUCCESS}, status=status.HTTP_200_OK)

        except (CustomException, pydantic.ValidationError) as e:
            return ProjectSubmissionErrorResponseFactory.create_response(exception=e)


class ProjectSubmissionRejectedView(APIView):
    @staticmethod
    def patch(request: Request, project_id: int) -> Response:
        print()
        logger.warning(f"PATCH /admin/project-submissions/{project_id}/reject/")
        try:
            user_id: Id = get_user_id_or_raises(request=request)
            gateway.project_submission_app_service.reject(user_id=user_id, project_id=Id(value=project_id))
            return Response({"code": SUCCESS}, status=status.HTTP_200_OK)
        except (CustomException, pydantic.ValidationError) as e:
            return ProjectSubmissionErrorResponseFactory.create_response(exception=e)
