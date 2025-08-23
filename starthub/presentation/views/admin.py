from dataclasses import asdict

import pydantic
from application.services.gateway import gateway
from domain.exceptions import CustomException
from domain.value_objects.common import Id
from infrastructure.auth.user import get_user_id_or_raises
from loguru import logger
from presentation.constants import SUCCESS
from presentation.request_converters.common import request_to_pagination
from presentation.response_factories.admin import ProjectSubmissionErrorResponseFactory
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class ProjectSubmissionGetView(APIView):
    @staticmethod
    def get(request: Request) -> Response:
        print()
        logger.info("GET /admin/projects/submissions")

        try:
            user_id = get_user_id_or_raises(request=request)
            pagination = request_to_pagination(request=request)
            projects = gateway.project_submission_app_service.get_submissions(user_id=user_id, pagination=pagination)
            return Response(list(map(asdict, projects)), status=status.HTTP_200_OK)
        except CustomException as e:
            return ProjectSubmissionErrorResponseFactory.create_response(exception=e)


class ProjectSubmissionApproveView(APIView):
    @staticmethod
    def patch(request: Request, project_id: int) -> Response:
        print()
        logger.warning(f"PATCH /admin/projects/submissions/{project_id}/approve/")
        try:
            user_id: Id = get_user_id_or_raises(request=request)
            gateway.project_submission_app_service.approve_submission(user_id=user_id, project_id=Id(value=project_id))
            return Response({"code": SUCCESS}, status=status.HTTP_200_OK)

        except (CustomException, pydantic.ValidationError) as e:
            return ProjectSubmissionErrorResponseFactory.create_response(exception=e)


class ProjectSubmissionRejectedView(APIView):
    @staticmethod
    def patch(request: Request, project_id: int) -> Response:
        print()
        logger.warning(f"PATCH /admin/projects/submissions/{project_id}/reject/")
        try:
            user_id: Id = get_user_id_or_raises(request=request)
            gateway.project_submission_app_service.reject_submission(user_id=user_id, project_id=Id(value=project_id))
            return Response({"code": SUCCESS}, status=status.HTTP_200_OK)
        except (CustomException, pydantic.ValidationError) as e:
            return ProjectSubmissionErrorResponseFactory.create_response(exception=e)


class ProjectDeactivateView(APIView):
    @staticmethod
    def patch(request: Request, project_id: int) -> Response:
        print()
        logger.warning(f"PATCH /admin/projects/{project_id}/deactivate/")
        try:
            user_id: Id = get_user_id_or_raises(request=request)
            gateway.project_submission_app_service.deactivate(user_id=user_id, project_id=Id(value=project_id))
            return Response({"code": SUCCESS}, status=status.HTTP_200_OK)
        except (CustomException, pydantic.ValidationError) as e:
            return ProjectSubmissionErrorResponseFactory.create_response(exception=e)
