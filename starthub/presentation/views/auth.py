from dataclasses import asdict

from application.dto.auth import AccessPayloadDto, AccessTokenDto, TokenPairDto
from application.service_factories.auth import AuthAppServiceFactory, RegistrationAppServiceFactory
from application.services.auth import AuthAppService, RegistrationAppService
from loguru import logger
from presentation.constants import SUCCESS
from presentation.response_factories.common import (
    CommonErrorResponseFactory,
    LoginErrorResponseFactory,
    RegistrationErrorResponseFactory,
)
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class LoginView(APIView):
    parser_classes = [JSONParser]
    error_classes: tuple[type[Exception], ...] = tuple(LoginErrorResponseFactory.error_codes.keys())

    def post(self, request: Request) -> Response:
        form_data: dict[str, str] = request.data
        logger.debug(f"request data = {form_data}")

        auth_service: AuthAppService = AuthAppServiceFactory.create_service()
        try:
            tokens_pair_dto: TokenPairDto = auth_service.login(form_data)
        except self.error_classes as e:
            logger.error(e)
            return LoginErrorResponseFactory.create_response(e)

        response = Response(data={"detail": "success", "code": SUCCESS}, status=200)
        response.set_cookie(
            "access_token",
            tokens_pair_dto.access_token,
            httponly=False,
            samesite="None",
            secure=True,
        )
        response.set_cookie(
            "refresh_token",
            tokens_pair_dto.refresh_token,
            httponly=True,
            samesite="None",
            secure=True,
        )
        logger.info("Tokens has been set to cookies.")

        return response


class RegistrationView(APIView):
    parser_classes = [JSONParser]
    error_classes: tuple[type[Exception], ...] = tuple(RegistrationErrorResponseFactory.error_codes.keys())

    def post(self, request: Request) -> Response:
        form_data: dict[str, str] = request.data
        registration_service: RegistrationAppService = RegistrationAppServiceFactory.create_service()
        try:
            registration_service.register(form_data)
        except self.error_classes as e:
            logger.error(e)
            return RegistrationErrorResponseFactory.create_response(e)

        return Response({"detail": "User has registered successfully.", "code": SUCCESS}, status.HTTP_201_CREATED)


class ReissueAccessTokenView(APIView):
    error_classes: tuple[type[Exception], ...] = tuple(CommonErrorResponseFactory.error_codes.keys())

    def post(self, request: Request) -> Response:
        auth_service: AuthAppService = AuthAppServiceFactory.create_service()

        try:
            access_token_dto: AccessTokenDto = auth_service.reissue_access(request.COOKIES)
        except self.error_classes as e:
            return CommonErrorResponseFactory.create_response(e)

        response = Response(data={"detail": "success", "code": SUCCESS}, status=200)
        response.set_cookie(
            "access_token",
            access_token_dto.access_token,
            httponly=False,
            samesite="None",
            secure=True,
        )
        return response


class AccessVerifyView(APIView):
    error_classes: tuple[type[Exception], ...] = tuple(CommonErrorResponseFactory.error_codes.keys())

    def post(self, request: Request) -> Response:
        auth_service: AuthAppService = AuthAppServiceFactory.create_service()

        try:
            access_payload_dto: AccessPayloadDto = auth_service.verify_access(request.COOKIES)
        except self.error_classes as e:
            return CommonErrorResponseFactory.create_response(e)

        return Response(asdict(access_payload_dto), status=status.HTTP_200_OK)


# TODO: Add logout
