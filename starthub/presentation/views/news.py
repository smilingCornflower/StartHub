from dataclasses import asdict

from application.dto.news import NewsDto
from application.services.gateway import gateway
from application.utils.get_access_payload_dto import get_access_payload_dto
from domain.models.news import News
from loguru import logger
from presentation.constants import SUCCESS
from presentation.response_factories.common import NewsErrorResponseFactory
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class NewsView(APIView):
    error_classes: tuple[type[Exception], ...] = tuple(NewsErrorResponseFactory.error_codes.keys())

    def get(self, request: Request, news_id: int | None = None) -> Response:
        logger.debug(f"GET /news/<news_id>/ \t news_id = {news_id}")
        try:
            news: list[NewsDto] = gateway.news_app_service.get(request_data=request.data, news_id=news_id)
            return Response(list(map(asdict, news)), status=status.HTTP_200_OK)
        except self.error_classes as e:
            logger.error(f"Exception: {repr(e)}")
            return NewsErrorResponseFactory.create_response(e)

    def post(self, request: Request) -> Response:
        logger.info(f"POST /news/ \n\t request.data: {request.data}\n\t request_files: {request.FILES}")

        try:
            access_dto = get_access_payload_dto(request.COOKIES)
            logger.debug(f"user_id = {int(access_dto.sub)}")
            news: News = gateway.news_app_service.create(
                request_data=request.data, request_files=request.FILES, user_id=int(access_dto.sub)
            )

        except self.error_classes as e:
            logger.error(f"Exception: {repr(e)}")
            return NewsErrorResponseFactory.create_response(e)

        return Response({"news_id": news.id, "code": "SUCCESS"}, status=status.HTTP_201_CREATED)

    def patch(self, request: Request, news_id: int) -> Response:
        logger.info(f"PATCH /news/{news_id}/ \n\t request.data = {request.data}")

        try:
            access_dto = get_access_payload_dto(request.COOKIES)
            gateway.news_app_service.update(request.data, request.FILES, news_id=news_id, user_id=int(access_dto.sub))

        except self.error_classes as e:
            logger.error(f"Exception: {repr(e)}")
            return NewsErrorResponseFactory.create_response(e)

        return Response({"detail": "news updated successfully", "code": "SUCCESS"}, status=status.HTTP_200_OK)

    def delete(self, request: Request, news_id: int) -> Response:
        logger.info(f"DELETE /news/{news_id}/")

        try:
            access_dto = get_access_payload_dto(request.COOKIES)
            gateway.news_app_service.delete(news_id=news_id, user_id=int(access_dto.sub))
            return Response({"detail": "News deleted.", "code": SUCCESS}, status=status.HTTP_200_OK)
        except self.error_classes as e:
            logger.error(f"Exception: {repr(e)}")
            return NewsErrorResponseFactory.create_response(e)
