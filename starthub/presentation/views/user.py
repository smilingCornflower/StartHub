from dataclasses import asdict
from venv import logger

import pydantic
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from application.dto.auth import AccessPayloadDto
from application.dto.project import ProjectDto
from application.dto.user import UserProfileDto
from application.services.gateway import gateway
from domain.exceptions import CustomException
from infrastructure.auth.token import get_access_payload_dto_from_headers
from presentation.constants import SUCCESS
from presentation.response_factories.common import UserErrorResponseFactory, UserFavoriteErrorResponseFactory


class UserView(APIView):
    @staticmethod
    def get(request: Request, user_id: int) -> Response:
        try:
            return Response(asdict(gateway.user_app_service.get_user_profile(user_id)), status=status.HTTP_200_OK)
        except CustomException as e:
            return UserErrorResponseFactory.create_response(e)


class MeView(APIView):
    parser_classes = [MultiPartParser]

    @staticmethod
    def patch(request: Request) -> Response:
        print()
        logger.info("PATCH /users/me")
        logger.debug(f"{request.data}")
        logger.debug(f"{request.FILES}")
        try:
            access_dto: AccessPayloadDto = get_access_payload_dto_from_headers(request.headers)
            gateway.user_app_service.update_user(request.data, request.FILES, int(access_dto.sub))
            return Response({"detail": "success", "code": SUCCESS}, status=status.HTTP_200_OK)
        except (CustomException, pydantic.ValidationError) as e:
            return UserErrorResponseFactory.create_response(e)

    @staticmethod
    def get(request: Request) -> Response:
        try:
            access_dto: AccessPayloadDto = get_access_payload_dto_from_headers(request.headers)
            user_profile_dto: UserProfileDto = gateway.user_app_service.get_user_own_profile(
                user_id=int(access_dto.sub)
            )
            return Response(asdict(user_profile_dto), status=status.HTTP_200_OK)
        except CustomException as e:
            return UserErrorResponseFactory.create_response(e)


class MeFavoriteProjectsView(APIView):
    @staticmethod
    def get(request: Request) -> Response:
        try:
            access_dto: AccessPayloadDto = get_access_payload_dto_from_headers(request.headers)
            user_favorite_projects: list[ProjectDto] = gateway.user_favorite_app_service.get_user_favorite_projects(
                user_id=int(access_dto.sub)
            )
            return Response(map(asdict, user_favorite_projects), status=status.HTTP_200_OK)
        except (CustomException, pydantic.ValidationError) as e:
            return UserErrorResponseFactory.create_response(e)

    @staticmethod
    def post(request: Request, project_id: int) -> Response:
        try:
            access_dto: AccessPayloadDto = get_access_payload_dto_from_headers(request.headers)
            gateway.user_favorite_app_service.add_favorite(user_id=int(access_dto.sub), project_id=project_id)
            return Response({"detail": "success", "code": SUCCESS}, status=status.HTTP_201_CREATED)

        except (CustomException, pydantic.ValidationError) as e:
            return UserFavoriteErrorResponseFactory.create_response(e)

    @staticmethod
    def delete(request: Request, project_id: int) -> Response:
        try:
            access_dto: AccessPayloadDto = get_access_payload_dto_from_headers(request.headers)
            gateway.user_favorite_app_service.delete_by_association_ids(int(access_dto.sub), project_id)
            return Response({"detail": "success", "code": SUCCESS}, status=status.HTTP_200_OK)
        except (CustomException, pydantic.ValidationError) as e:
            return UserFavoriteErrorResponseFactory.create_response(e)


class UserFavoriteProjectsView(APIView):
    @staticmethod
    def get(request: Request, user_id: int) -> Response:
        try:
            user_favorite_projects: list[ProjectDto] = gateway.user_favorite_app_service.get_user_favorite_projects(
                user_id=user_id
            )
            return Response(map(asdict, user_favorite_projects), status=status.HTTP_200_OK)
        except CustomException as e:
            return UserErrorResponseFactory.create_response(e)
