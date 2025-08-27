from dataclasses import asdict

from application.dto.notification import NotificationDto
from application.services.gateway import gateway
from domain.exceptions import CustomException
from domain.value_objects.common import Id
from infrastructure.auth.user import get_user_id_or_raises
from loguru import logger
from presentation.request_converters.common import request_to_cursor_pagination
from presentation.request_converters.notification import request_to_notification_get_command
from presentation.response_factories.notification import NotificationErrorResponseFactory
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class NotificationView(APIView):
    @staticmethod
    def get(request: Request, target_user_id: int) -> Response:
        print()
        logger.info(f"GET /notifications/{target_user_id}/")

        try:
            caller_user_id: Id = get_user_id_or_raises(request=request)
            pagination = request_to_cursor_pagination(request=request)
            notification_get_command = request_to_notification_get_command(request=request)

            notifications: list[NotificationDto] = gateway.notification_app_service.get_all(
                caller_user_id=caller_user_id,
                target_user_id=Id(value=target_user_id),
                command=notification_get_command,
                pagniation=pagination,
            )
            return Response(list(map(asdict, notifications)), status=status.HTTP_200_OK)
        except CustomException as e:
            return NotificationErrorResponseFactory.create_response(exception=e)
