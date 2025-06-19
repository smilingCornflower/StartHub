from application.services.gateway import gateway
from application.utils.get_access_payload_dto import get_access_payload_dto
from domain.models.news import News
from loguru import logger
from presentation.response_factories.common import NewsErrorResponseFactory
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class NewsView(APIView):
    error_classes: tuple[type[Exception], ...] = tuple(NewsErrorResponseFactory.error_codes.keys())

    def post(self, request: Request) -> Response:
        logger.info(f"POST /news/ \n\t request.data: {request.data}\n\t request_files: {request.FILES}")

        try:
            access_dto = get_access_payload_dto(request.COOKIES)
            logger.debug(f"user_id = {int(access_dto.sub)}")
            news: News = gateway.news_app_service.create(
                request_data=request.data, request_files=request.FILES, user_id=int(access_dto.sub)
            )

        except self.error_classes as e:
            logger.error(f"Exception: {e}")
            return NewsErrorResponseFactory.create_response(e)

        return Response({"news_id": news.id, "code": "SUCCESS"}, status=status.HTTP_201_CREATED)
