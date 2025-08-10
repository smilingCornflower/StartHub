from application.services.gateway import gateway
from domain.exceptions import CustomException
from domain.value_objects.common import Id
from domain.value_objects.project.accelerator import ProjectAcceleratorCreateCommand
from infrastructure.auth.user import get_user_id_or_raises
from presentation.constants import SUCCESS
from presentation.request_converters.project.accelerator import request_to_project_accelerator_create_command
from presentation.response_factories.common import AcceleratorErrorResponseFactory
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class AcceleratorView(APIView):
    def post(self, request: Request, project_id: int) -> Response:
        try:
            user_id: Id = get_user_id_or_raises(request=request)
            command: ProjectAcceleratorCreateCommand = request_to_project_accelerator_create_command(request=request)
            gateway.accelerator_app_service.create(user_id=user_id, project_id=Id(value=project_id), command=command)
            return Response({"code": SUCCESS}, status=status.HTTP_200_OK)
        except CustomException as e:
            return AcceleratorErrorResponseFactory.create_response(exception=e)

    def delete(self, request: Request, project_id: int) -> Response:
        try:
            user_id: Id = get_user_id_or_raises(request=request)
            gateway.accelerator_app_service.delete(user_id=user_id, project_id=Id(value=project_id))
            return Response({"code": SUCCESS}, status=status.HTTP_200_OK)

        except CustomException as e:
            return AcceleratorErrorResponseFactory.create_response(exception=e)
