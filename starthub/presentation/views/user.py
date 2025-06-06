from application.dto.auth import AccessPayloadDto
from application.services.gateway import Gateway
from application.utils.get_access_payload_dto import get_access_payload_dto
from loguru import logger
from presentation.response_factories.common import CommonErrorResponseFactory
from rest_framework.parsers import MultiPartParser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class UserProfile(APIView):
    parser_classes = [MultiPartParser]
    error_classes: tuple[type[Exception], ...] = tuple(CommonErrorResponseFactory.error_codes.keys())

    def post(self, request: Request) -> Response:
        try:
            access_dto: AccessPayloadDto = get_access_payload_dto(request.COOKIES)
        except self.error_classes as e:
            logger.error(f"Exception: {e}")
            return CommonErrorResponseFactory.create_response(e)

        Gateway.user_app_service.upload_profile_picture(request.FILES, int(access_dto.sub))

        return Response({"detail": "success"}, 200)
