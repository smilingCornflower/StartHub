from application.services.gateway import gateway
from domain.exceptions import CustomException
from domain.value_objects.common import Id
from domain.value_objects.project.accelerator import AcceleratorId
from infrastructure.auth.user import get_user_id_or_raises
from presentation.constants import SUCCESS
from presentation.response_factories.common import AcceleratorErrorResponseFactory
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class AcceleratorView(APIView):
    def delete(self, request: Request, accelerator_id: int) -> Response:
        try:
            user_id: Id = get_user_id_or_raises(request=request)
            gateway.accelerator_app_service.delete(user_id=user_id, accelerator_id=AcceleratorId(value=accelerator_id))
            return Response({"code": SUCCESS}, status=status.HTTP_200_OK)

        except CustomException as e:
            return AcceleratorErrorResponseFactory.create_response(exception=e)
