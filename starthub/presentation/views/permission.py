from dataclasses import asdict

from application.services.gateway import gateway
from domain.enums.role import RoleEnum
from domain.exceptions import CustomException
from domain.value_objects.common import Id
from loguru import logger
from presentation.helpers.auth import get_authenticated_user_from_request
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
            user = get_authenticated_user_from_request(request=request)
            user_id = Id(value=user.id)

            role_name: RoleEnum | None = get_role_if_exists_from_params(params=request.query_params)
            logger.debug(f"role name = {role_name}")
            permissions = gateway.permission_app_service.get(user_id=user_id, role_name=role_name)
            return Response(list(map(asdict, permissions)), status=status.HTTP_200_OK)
        except CustomException as e:
            return PermissionErrorResponseFactory.create_response(exception=e)
