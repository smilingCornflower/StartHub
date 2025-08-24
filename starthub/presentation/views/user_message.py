import pydantic
from application.services.gateway import gateway
from domain.exceptions import CustomException
from infrastructure.auth.user import get_user_id_or_raises
from loguru import logger
from presentation.constants import SUCCESS
from presentation.request_converters.user_management.user_message import request_to_user_message_create_command
from presentation.response_factories.user_management import UserMessageErrorResponseFactory
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class UserMessageView(APIView):
    @staticmethod
    def post(request: Request) -> Response:
        print()
        logger.info("POST /users/messages/")

        try:
            user_id = get_user_id_or_raises(request=request)
            command = request_to_user_message_create_command(request=request)
            gateway.user_message_app_service.create(user_id=user_id, command=command)

            return Response({"code": SUCCESS}, status=status.HTTP_201_CREATED)

        except (CustomException, pydantic.ValidationError) as e:
            return UserMessageErrorResponseFactory.create_response(exception=e)
