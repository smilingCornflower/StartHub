from dataclasses import asdict
from typing import cast

from application.dto.auth import AccessPayloadDto, AccessTokenDto, TokenPairDto
from application.ports.cookie_service import CookiesResponseProtocol
from application.services.gateway import gateway
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
        logger.info("POST /auth/login/")
        try:
            tokens_pair_dto: TokenPairDto = gateway.auth_app_service.login(request.data)
        except self.error_classes as e:
            logger.error(e)
            return LoginErrorResponseFactory.create_response(e)

        response = Response(data={"detail": "success", "code": SUCCESS}, status=200)

        gateway.cookie_service.set_access_token_to_cookies(
            cast(CookiesResponseProtocol, response), tokens_pair_dto.access_token
        )
        gateway.cookie_service.set_refresh_token_to_cookies(
            cast(CookiesResponseProtocol, response), tokens_pair_dto.refresh_token
        )
        logger.info("Tokens has been set to cookies.")
        # C:\Users\Smile\Main\Projects\2025\StartHub\starthub\presentation\views\auth.py:34: error: Argument 1 to "set_access_token_to_cookies" of "CookieService" has incompatible type "Response"; expected "CookiesResponseProtocol"  [arg-type]

        return response


class RegistrationView(APIView):
    parser_classes = [JSONParser]
    error_classes: tuple[type[Exception], ...] = tuple(RegistrationErrorResponseFactory.error_codes.keys())

    def post(self, request: Request) -> Response:
        logger.info("POST /auth/register/")
        try:
            gateway.registration_app_service.register(request.data)
        except self.error_classes as e:
            logger.error(e)
            return RegistrationErrorResponseFactory.create_response(e)

        return Response({"detail": "User has registered successfully.", "code": SUCCESS}, status.HTTP_201_CREATED)


class ReissueAccessTokenView(APIView):
    error_classes: tuple[type[Exception], ...] = tuple(CommonErrorResponseFactory.error_codes.keys())

    def post(self, request: Request) -> Response:
        logger.debug("POST /auth/reissue-access/")
        try:
            access_token_dto: AccessTokenDto = gateway.auth_app_service.reissue_access(request.COOKIES)
        except self.error_classes as e:
            return CommonErrorResponseFactory.create_response(e)

        response = Response(data={"detail": "success", "code": SUCCESS}, status=200)
        gateway.cookie_service.set_access_token_to_cookies(
            cast(CookiesResponseProtocol, response), access_token_dto.access_token
        )
        logger.debug("Access token has set to cookies")
        return response


class AccessVerifyView(APIView):
    error_classes: tuple[type[Exception], ...] = tuple(CommonErrorResponseFactory.error_codes.keys())

    def post(self, request: Request) -> Response:
        logger.debug("POST /auth/verify-access/")
        try:
            access_payload_dto: AccessPayloadDto = gateway.auth_app_service.verify_access(request.COOKIES)
        except self.error_classes as e:
            return CommonErrorResponseFactory.create_response(e)

        return Response(asdict(access_payload_dto), status=status.HTTP_200_OK)


class LogoutView(APIView):
    error_classes: tuple[type[Exception], ...] = tuple(CommonErrorResponseFactory.error_codes.keys())

    def post(self, request: Request) -> Response:
        logger.info("POST /auth/logout/")
        try:
            response = Response({"detail": SUCCESS}, status.HTTP_200_OK)
            gateway.cookie_service.remove_access_token_from_cookies(response=cast(CookiesResponseProtocol, response))
            gateway.cookie_service.remove_refresh_token_from_cookies(response=cast(CookiesResponseProtocol, response))
        except self.error_classes as e:
            return CommonErrorResponseFactory.create_response(e)

        return response
