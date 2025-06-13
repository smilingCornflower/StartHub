from dataclasses import asdict

from application.dto.auth import AccessPayloadDto
from application.dto.user import UserFavoriteDto, UserProfileDto
from application.services.gateway import gateway
from application.utils.get_access_payload_dto import get_access_payload_dto
from loguru import logger
from presentation.constants import SUCCESS
from presentation.response_factories.common import UserErrorResponseFactory, UserFavoriteResponseFactory
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class UserView(APIView):
    error_classes: tuple[type[Exception], ...] = tuple(UserErrorResponseFactory.error_codes.keys())

    def get(self, request: Request, user_id: int) -> Response:
        try:
            return Response(asdict(gateway.user_app_service.get_user_profile(user_id)), status=status.HTTP_200_OK)
        except self.error_classes as e:
            logger.exception(f"Exception: {repr(e)}")
            return UserErrorResponseFactory.create_response(e)


class MeView(APIView):
    parser_classes = [MultiPartParser]
    error_classes: tuple[type[Exception], ...] = tuple(UserErrorResponseFactory.error_codes.keys())

    def patch(self, request: Request) -> Response:
        try:
            access_dto: AccessPayloadDto = get_access_payload_dto(request.COOKIES)
            gateway.user_app_service.update_user(request.data, request.FILES, int(access_dto.sub))
            return Response({"detail": "success", "code": SUCCESS}, status=status.HTTP_200_OK)
        except self.error_classes as e:
            logger.error(f"Exception: {repr(e)}")
            return UserErrorResponseFactory.create_response(e)

    def get(self, request: Request) -> Response:
        try:
            access_dto: AccessPayloadDto = get_access_payload_dto(request.COOKIES)
            user_profile_dto: UserProfileDto = gateway.user_app_service.get_user_own_profile(
                user_id=int(access_dto.sub)
            )
            return Response(asdict(user_profile_dto), status=status.HTTP_200_OK)
        except self.error_classes as e:
            logger.error(f"Exception: {repr(e)}")
            return UserErrorResponseFactory.create_response(e)


class MeFavoriteProjectsView(APIView):
    error_classes: tuple[type[Exception], ...] = tuple(UserFavoriteResponseFactory.error_codes.keys())

    def get(self, request: Request) -> Response:
        try:
            access_dto: AccessPayloadDto = get_access_payload_dto(request.COOKIES)
            user_favorites: list[UserFavoriteDto] = gateway.user_favorite_app_service.get_user_favorites(
                user_id=int(access_dto.sub)
            )
            return Response(map(asdict, user_favorites), status=status.HTTP_200_OK)
        except self.error_classes as e:
            logger.error(f"Exception: {repr(e)}")
            return UserErrorResponseFactory.create_response(e)

    def post(self, request: Request, project_id: int) -> Response:
        try:
            access_dto: AccessPayloadDto = get_access_payload_dto(request.COOKIES)
            gateway.user_favorite_app_service.add_favorite(user_id=int(access_dto.sub), project_id=project_id)
            return Response({"detail": "success", "code": SUCCESS}, status=status.HTTP_201_CREATED)

        except self.error_classes as e:
            logger.error(f"Exception: {repr(e)}")
            return UserFavoriteResponseFactory.create_response(e)

    def delete(self, request: Request, project_id: int) -> Response:
        try:
            access_dto: AccessPayloadDto = get_access_payload_dto(request.COOKIES)
            gateway.user_favorite_app_service.delete_by_association_ids(int(access_dto.sub), project_id)
            return Response({"detail": "success", "code": SUCCESS}, status=status.HTTP_200_OK)
        except self.error_classes as e:
            logger.error(f"Exception: {repr(e)}")
            return UserFavoriteResponseFactory.create_response(e)

class UserFavoriteProjectsView(APIView):
    error_classes: tuple[type[Exception], ...] = tuple(UserFavoriteResponseFactory.error_codes.keys())

    def get(self, request: Request, user_id: int) -> Response:
        try:
            user_favorites: list[UserFavoriteDto] = gateway.user_favorite_app_service.get_user_favorites(user_id=user_id)
            return Response(map(asdict, user_favorites), status=status.HTTP_200_OK)
        except self.error_classes as e:
            logger.error(f"Exception: {repr(e)}")
            return UserErrorResponseFactory.create_response(e)