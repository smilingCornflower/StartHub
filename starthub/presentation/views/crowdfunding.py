from application.services.gateway import gateway
from domain.exceptions import CustomException
from domain.value_objects.common import Id
from infrastructure.auth.user import get_user_id_or_raises
from presentation.constants import SUCCESS
from presentation.request_converters.project.crowdfunding import (
    request_to_project_crowdfunding_create_command,
    request_to_project_crowdfunding_update_command,
)
from presentation.response_factories.project_management import CrowdfundingErrorResponseFactory
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class CrowdfundingView(APIView):
    def post(self, request: Request, project_id: int) -> Response:
        try:
            user_id: Id = get_user_id_or_raises(request=request)
            command = request_to_project_crowdfunding_create_command(request=request)
            gateway.crowdfunding_app_service.create(user_id=user_id, project_id=Id(value=project_id), command=command)

            return Response({"code": SUCCESS}, status=status.HTTP_200_OK)

        except CustomException as e:
            return CrowdfundingErrorResponseFactory.create_response(exception=e)

    def delete(self, request: Request, project_id: int) -> Response:
        try:
            user_id: Id = get_user_id_or_raises(request=request)
            gateway.crowdfunding_app_service.delete(user_id=user_id, project_id=Id(value=project_id))
            return Response({"code": SUCCESS}, status=status.HTTP_200_OK)
        except CustomException as e:
            return CrowdfundingErrorResponseFactory.create_response(exception=e)

    def patch(self, request: Request, project_id: int) -> Response:
        try:
            user_id: Id = get_user_id_or_raises(request=request)
            command = request_to_project_crowdfunding_update_command(request=request)
            gateway.crowdfunding_app_service.update(user_id=user_id, project_id=Id(value=project_id), command=command)
            return Response({"code": SUCCESS}, status=status.HTTP_200_OK)
        except CustomException as e:
            return CrowdfundingErrorResponseFactory.create_response(exception=e)
