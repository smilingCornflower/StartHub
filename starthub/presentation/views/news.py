from dataclasses import asdict

import pydantic
from application.dto.news import NewsFullDto, NewsShortDto
from application.services.gateway import gateway
from domain.exceptions import CustomException
from domain.value_objects.common import Pagination
from infrastructure.auth.token import get_access_payload_dto_from_headers
from loguru import logger
from presentation.constants import SUCCESS
from presentation.request_converters.common import request_to_pagination
from presentation.response_factories.common import NewsErrorResponseFactory
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class NewsView(APIView):
    @staticmethod
    def get(request: Request, news_id: int | None = None) -> Response:
        logger.debug(f"GET /news/<news_id>/ \t news_id = {news_id}")
        try:
            if news_id:
                news: NewsFullDto | list[NewsShortDto] = gateway.news_app_service.get(news_id=news_id)
            else:
                pagination: Pagination = request_to_pagination(request=request)
                news = gateway.news_app_service.get(pagination=pagination)

            if isinstance(news, NewsFullDto):
                return Response(asdict(news), status=status.HTTP_200_OK)
            return Response(list(map(asdict, news)), status=status.HTTP_200_OK)

        except CustomException as e:
            return NewsErrorResponseFactory.create_response(e)

    @staticmethod
    def post(request: Request) -> Response:
        logger.info(f"POST /news/ \n\t request.data: {request.data}\n\t request_files: {request.FILES}")

        try:
            access_dto = get_access_payload_dto_from_headers(request.headers)
            logger.debug(f"user_id = {int(access_dto.sub)}")
            news_id: int = gateway.news_app_service.create(
                request_data=request.data, request_files=request.FILES, user_id=int(access_dto.sub)
            )

        except (CustomException, pydantic.ValidationError) as e:
            return NewsErrorResponseFactory.create_response(e)

        return Response({"news_id": news_id, "code": "SUCCESS"}, status=status.HTTP_201_CREATED)

    @staticmethod
    def patch(request: Request, news_id: int) -> Response:
        logger.debug("PATCH /news/{news_id}/ \n\t request.data = {request.data}")

        try:
            access_dto = get_access_payload_dto_from_headers(request.headers)
            gateway.news_app_service.update(request.data, request.FILES, news_id=news_id, user_id=int(access_dto.sub))

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
