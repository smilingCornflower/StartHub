from dataclasses import asdict

import pydantic
from application.dto.news import NewsFullDto, NewsShortDto
from application.services.gateway import gateway
from domain.exceptions import CustomException
from domain.value_objects.common import Id, OffsetPagination
from infrastructure.auth.token import get_access_payload_dto_from_headers
from infrastructure.auth.user import get_user_id_or_raises
from loguru import logger
from presentation.constants import SUCCESS
from presentation.request_converters.common import request_to_offset_pagination
from presentation.request_converters.news import (
    request_to_news_create_command,
    request_to_news_get_command,
    request_to_news_tag_name,
    request_to_news_update_command,
)
from presentation.response_factories.news import NewsErrorResponseFactory
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class NewsView(APIView):
    @staticmethod
    def get(request: Request, news_id: int | None = None) -> Response:
        print()
        logger.debug(f"GET /news/<news_id>/ \t news_id = {news_id}")
        try:
            if news_id:
                news: NewsFullDto | list[NewsShortDto] = gateway.news_app_service.get_one(news_id=news_id)
            else:
                command = request_to_news_get_command(request=request)
                pagination: OffsetPagination = request_to_offset_pagination(request=request)
                news = gateway.news_app_service.get_many(pagination=pagination, command=command)
            if isinstance(news, NewsFullDto):
                return Response(asdict(news), status=status.HTTP_200_OK)

            return Response(list(map(asdict, news)), status=status.HTTP_200_OK)

        except CustomException as e:
            return NewsErrorResponseFactory.create_response(e)

    @staticmethod
    def post(request: Request) -> Response:
        print()
        logger.info(f"POST /news/\n" f"request.data: {request.data}\n" f"request_files: {request.FILES}")

        try:
            user_id = get_user_id_or_raises(request=request)

            command = request_to_news_create_command(request=request, user_id=user_id)
            news_id: int = gateway.news_app_service.create(user_id=user_id, news_create_command=command)

        except (CustomException, pydantic.ValidationError) as e:
            return NewsErrorResponseFactory.create_response(e)

        return Response({"news_id": news_id, "code": "SUCCESS"}, status=status.HTTP_201_CREATED)

    @staticmethod
    def patch(request: Request, news_id: int) -> Response:
        logger.debug("PATCH /news/{news_id}/ \n\t request.data = {request.data}")

        try:
            user_id = get_user_id_or_raises(request=request)
            command = request_to_news_update_command(request=request)
            gateway.news_app_service.update(update_command=command, news_id=Id(value=news_id), user_id=user_id)

        except (CustomException, pydantic.ValidationError) as e:
            return NewsErrorResponseFactory.create_response(e)

        return Response({"detail": "news updated successfully", "code": "SUCCESS"}, status=status.HTTP_200_OK)

    @staticmethod
    def delete(request: Request, news_id: int) -> Response:
        logger.info(f"DELETE /news/{news_id}/")

        try:
            access_dto = get_access_payload_dto_from_headers(request.headers)
            gateway.news_app_service.delete(news_id=news_id, user_id=int(access_dto.sub))
            return Response({"detail": "News deleted.", "code": SUCCESS}, status=status.HTTP_200_OK)
        except CustomException as e:
            return NewsErrorResponseFactory.create_response(e)


class NewsActivateView(APIView):
    @staticmethod
    def patch(request: Request, news_id: int) -> Response:
        print()
        logger.info(f"PATCH /news/{news_id}/activate/")

        try:
            user_id = get_user_id_or_raises(request=request)
            gateway.news_app_service.activate(user_id=user_id, news_id=Id(value=news_id))
            return Response({"code": SUCCESS}, status=status.HTTP_200_OK)
        except CustomException as e:
            return NewsErrorResponseFactory.create_response(e)


class NewsDeactivateView(APIView):
    @staticmethod
    def patch(request: Request, news_id: int) -> Response:
        print()
        logger.info(f"PATCH /news/{news_id}/deactivate/")

        try:
            user_id = get_user_id_or_raises(request=request)
            gateway.news_app_service.deactivate(user_id=user_id, news_id=Id(value=news_id))
            return Response({"code": SUCCESS}, status=status.HTTP_200_OK)

        except CustomException as e:
            return NewsErrorResponseFactory.create_response(e)


class NewsTagView(APIView):
    @staticmethod
    def delete(request: Request, news_id: int, tag_name: str) -> Response:
        print()
        logger.info(f"DELETE /news/{news_id}/tags/{tag_name}/")

        try:
            user_id = get_user_id_or_raises(request=request)
            gateway.news_tag_app_service.delete_tag_from_news(
                user_id=user_id, news_id=Id(value=news_id), tag_name=tag_name
            )
            return Response({"code": SUCCESS}, status=status.HTTP_200_OK)
        except CustomException as e:
            return NewsErrorResponseFactory.create_response(exception=e)

    @staticmethod
    def post(request: Request, news_id: int) -> Response:
        print()
        logger.info(f"POST /news/{news_id}/tags/")
        try:
            user_id = get_user_id_or_raises(request=request)
            tag_name = request_to_news_tag_name(request=request)
            gateway.news_tag_app_service.add_tag_to_news(user_id=user_id, news_id=Id(value=news_id), tag_name=tag_name)
            return Response({"code": SUCCESS}, status=status.HTTP_201_CREATED)
        except (CustomException, pydantic.ValidationError) as e:
            return NewsErrorResponseFactory.create_response(exception=e)
