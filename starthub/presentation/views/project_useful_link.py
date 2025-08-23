from application.services.gateway import gateway
from domain.exceptions import CustomException
from domain.value_objects.common import Id
from domain.value_objects.project.useful_link import UsefulLinkId
from infrastructure.auth.user import get_user_id_or_raises
from presentation.constants import SUCCESS
from presentation.request_converters.project.useful_link import (
    request_to_useful_link_create_command,
    request_to_useful_link_update_command,
)
from presentation.response_factories.common import ProjectUsefulLinkErrorResponseFactory
from pydantic import ValidationError
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class ProjectUsefulLinkView(APIView):
    @staticmethod
    def post(request: Request, project_id: int) -> Response:
        try:
            user_id: Id = get_user_id_or_raises(request=request)
            command = request_to_useful_link_create_command(request=request)
            gateway.project_useful_link_app_service.create(
                user_id=user_id, project_id=Id(value=project_id), command=command
            )

            return Response({"code": SUCCESS}, status=status.HTTP_201_CREATED)
        except (CustomException, ValidationError) as e:
            return ProjectUsefulLinkErrorResponseFactory.create_response(exception=e)

    @staticmethod
    def patch(request: Request, useful_link_id: int) -> Response:
        try:
            user_id: Id = get_user_id_or_raises(request=request)
            command = request_to_useful_link_update_command(request=request)
            gateway.project_useful_link_app_service.update(
                user_id=user_id, useful_link_id=UsefulLinkId(value=useful_link_id), command=command
            )

            return Response({"code": SUCCESS}, status=status.HTTP_200_OK)
        except (CustomException, ValidationError) as e:
            return ProjectUsefulLinkErrorResponseFactory.create_response(exception=e)

    @staticmethod
    def delete(request: Request, useful_link_id: int) -> Response:
        try:
            user_id: Id = get_user_id_or_raises(request=request)
            gateway.project_useful_link_app_service.delete(
                user_id=user_id, useful_link_id=UsefulLinkId(value=useful_link_id)
            )

            return Response({"code": SUCCESS}, status=status.HTTP_200_OK)
        except (CustomException, ValidationError) as e:
            return ProjectUsefulLinkErrorResponseFactory.create_response(exception=e)
