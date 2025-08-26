from dataclasses import asdict

from application.services.gateway import gateway
from domain.enums.role import RoleEnum
from domain.exceptions import CustomException
from infrastructure.auth.user import get_user_id_or_raises
from loguru import logger
from presentation.request_converters.common import get_role_if_exists_from_params
from presentation.response_factories.permission import PermissionErrorResponseFactory
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class PermissionView(APIView):
    @staticmethod
    def get(request: Request) -> Response:
        print()
        logger.info("GET /permissions/")
        try:
            user_id = get_user_id_or_raises(request=request)
            role_name: RoleEnum | None = get_role_if_exists_from_params(params=request.query_params)
            logger.debug(f"role name = {role_name}")
            permissions = gateway.permission_app_service.get(user_id=user_id, role_name=role_name)
            return Response(list(map(asdict, permissions)), status=status.HTTP_200_OK)
        except CustomException as e:
            return PermissionErrorResponseFactory.create_response(exception=e)
