from dataclasses import asdict

import pydantic
from application.services.gateway import gateway
from domain.exceptions import CustomException
from domain.value_objects.common import Id
from domain.value_objects.user_management.user_admin import UserAdminUpdateCommand
from infrastructure.auth.user import get_user_id_or_raises
from loguru import logger
from presentation.constants import SUCCESS
from presentation.request_converters.common import request_to_cursor_pagination
from presentation.request_converters.project.submission import request_to_project_submission_reject_command
from presentation.request_converters.user_management.user import request_to_user_get_command
from presentation.request_converters.user_management.user_admin import request_to_user_admin_update_command
from presentation.response_factories.admin import ProjectSubmissionErrorResponseFactory
from presentation.response_factories.user_management import UsersAdminErrorResponseFactory
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
            pagination = request_to_cursor_pagination(request=request)
            projects = gateway.projects_admin_app_service.get_submissions(user_id=user_id, pagination=pagination)
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
            gateway.projects_admin_app_service.approve_submission(user_id=user_id, project_id=Id(value=project_id))
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
            command = request_to_project_submission_reject_command(request=request)
            gateway.projects_admin_app_service.reject_submission(
                user_id=user_id, project_id=Id(value=project_id), command=command
            )
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
            gateway.projects_admin_app_service.deactivate(user_id=user_id, project_id=Id(value=project_id))
            return Response({"code": SUCCESS}, status=status.HTTP_200_OK)
        except (CustomException, pydantic.ValidationError) as e:
            return ProjectSubmissionErrorResponseFactory.create_response(exception=e)


class UsersAdminView(APIView):
    @staticmethod
    def patch(request: Request, target_user_id: int) -> Response:
        print()
        logger.warning(f"PATCH /admin/users/{target_user_id}/")

        try:
            caller_user_id: Id = get_user_id_or_raises(request=request)
            command: UserAdminUpdateCommand = request_to_user_admin_update_command(request=request)
            gateway.user_admin_app_service.change_user_role(
                call_user_id=caller_user_id, target_user_id=Id(value=target_user_id), command=command
            )
            return Response({"code": SUCCESS}, status=status.HTTP_200_OK)

        except (CustomException, pydantic.ValidationError) as e:
            return UsersAdminErrorResponseFactory.create_response(exception=e)


class UserAdminDeactivateView(APIView):
    @staticmethod
    def patch(request: Request, target_user_id: int) -> Response:
        print()
        logger.warning(f"PATCH /admin/users/{target_user_id}/deactivate/")

        try:
            caller_user_id: Id = get_user_id_or_raises(request=request)
            gateway.user_admin_app_service.deactivate_user(
                call_user_id=caller_user_id, target_user_id=Id(value=target_user_id)
            )
            return Response({"code": SUCCESS}, status=status.HTTP_200_OK)
        except CustomException as e:
            return UsersAdminErrorResponseFactory.create_response(exception=e)


class UserAdminActivateView(APIView):
    @staticmethod
    def patch(request: Request, target_user_id: int) -> Response:
        print()
        logger.warning(f"PATCH /admin/users/{target_user_id}/activate/")

        try:
            caller_user_id: Id = get_user_id_or_raises(request=request)
            gateway.user_admin_app_service.activate_user(
                call_user_id=caller_user_id, target_user_id=Id(value=target_user_id)
            )
            return Response({"code": SUCCESS}, status=status.HTTP_200_OK)
        except CustomException as e:
            return UsersAdminErrorResponseFactory.create_response(exception=e)


class UserDetailView(APIView):
    @staticmethod
    def get(request: Request) -> Response:
        print()
        logger.info("GET /users/")
        try:
            user_id = get_user_id_or_raises(request=request)
            pagination = request_to_cursor_pagination(request=request)
            command = request_to_user_get_command(request=request)
            users = gateway.user_admin_get_app_service.get_all(user_id, command, pagination)
            return Response(list(map(asdict, users)), status=status.HTTP_200_OK)

        except (CustomException, pydantic.ValidationError) as e:
            return UsersAdminErrorResponseFactory.create_response(exception=e)
