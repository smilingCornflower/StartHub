from dataclasses import asdict

import pydantic
from application.services.gateway import gateway
from domain.exceptions import CustomException
from domain.value_objects.common import Id
from loguru import logger
from presentation.constants import SUCCESS
from presentation.helpers.auth import get_authenticated_user_from_request
from presentation.request_converters.common import request_to_cursor_pagination
from presentation.request_converters.user_management.user_message import (
    request_to_user_message_create_command,
    request_to_user_message_get_command,
)
from presentation.response_factories.user_management import UserMessageErrorResponseFactory
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class UserMessageView(APIView):
    @staticmethod
    def get(request: Request) -> Response:
        print()
        logger.info("GET /users/messages/")

        try:
            user = get_authenticated_user_from_request(request=request)
            user_id = Id(value=user.id)
            pagination = request_to_cursor_pagination(request=request)
            command = request_to_user_message_get_command(request=request)
            messages = gateway.user_message_app_service.get(user_id=user_id, command=command, pagination=pagination)
            return Response(list(map(asdict, messages)), status=status.HTTP_200_OK)
        except (CustomException, pydantic.ValidationError) as e:
            return UserMessageErrorResponseFactory.create_response(exception=e)

    @staticmethod
    def post(request: Request) -> Response:
        print()
        logger.info("POST /users/messages/")

        try:
            user = get_authenticated_user_from_request(request=request)
            user_id = Id(value=user.id)
            command = request_to_user_message_create_command(request=request)
            gateway.user_message_app_service.create(user_id=user_id, command=command)

            return Response({"code": SUCCESS}, status=status.HTTP_201_CREATED)

        except (CustomException, pydantic.ValidationError) as e:
            return UserMessageErrorResponseFactory.create_response(exception=e)


class MeUserMessageView(APIView):
    @staticmethod
    def get(request: Request) -> Response:
        print()
        logger.info("GET /users/me/messages/")

        try:
            user = get_authenticated_user_from_request(request=request)
            user_id = Id(value=user.id)
            pagination = request_to_cursor_pagination(request=request)
            command = request_to_user_message_get_command(request=request)
            messages = gateway.user_message_app_service.get_my(user_id=user_id, command=command, pagination=pagination)
            return Response(list(map(asdict, messages)), status=status.HTTP_200_OK)

        except (CustomException, pydantic.ValidationError) as e:
            return UserMessageErrorResponseFactory.create_response(exception=e)
