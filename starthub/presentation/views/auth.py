from dataclasses import asdict
from typing import cast

import pydantic
from application.dto.auth import AccessPayloadDto, AccessTokenDto, TokenPairDto
from application.ports.cookie_service import CookiesResponseProtocol
from application.services.gateway import gateway
from domain.exceptions import DomainException
from loguru import logger
from presentation.constants import SUCCESS
from presentation.response_factories.common import (
    CommonErrorResponseFactory,
    LoginErrorResponseFactory,
    RegistrationErrorResponseFactory,
    ReissueAccessErrorResponseFactory,
)
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class LoginView(APIView):
    parser_classes = [JSONParser]
    @staticmethod
    def post(request: Request) -> Response:
        origin = request.headers.get("Origin")
        referer = request.headers.get("Referer")
        logger.info(f"POST /auth/login/ Origin: {origin}, Referer: {referer}")

        logger.info("POST /auth/login/")
        try:
            tokens_pair_dto: TokenPairDto = gateway.auth_app_service.login(request.data)
        except (DomainException, pydantic.ValidationError) as e:
            return LoginErrorResponseFactory.create_response(e)

        response = Response(data={"access_token": tokens_pair_dto.access_token, "code": SUCCESS}, status=200)
        gateway.cookie_service.set_refresh_token_to_cookies(
            cast(CookiesResponseProtocol, response), tokens_pair_dto.refresh_token
        )

        logger.info("Refresh has been set to cookies.")
        return response


class RegistrationView(APIView):
    parser_classes = [JSONParser]

    @staticmethod
    def post(request: Request) -> Response:
        logger.info("POST /auth/register/")
        try:
            gateway.registration_app_service.register(request.data)
        except (DomainException, pydantic.ValidationError) as e:
            return RegistrationErrorResponseFactory.create_response(e)

        return Response({"detail": "User has registered successfully.", "code": SUCCESS}, status.HTTP_201_CREATED)


class ReissueAccessTokenView(APIView):
    @staticmethod
    def post(request: Request) -> Response:
        logger.debug("POST /auth/reissue-access/")
        try:
            access_token_dto: AccessTokenDto = gateway.auth_app_service.reissue_access(request.COOKIES)
            return Response({"access_token": access_token_dto.access_token, "code": SUCCESS}, status=status.HTTP_200_OK)
        except (DomainException, pydantic.ValidationError) as e:
            return ReissueAccessErrorResponseFactory.create_response(e)


class AccessVerifyView(APIView):
    @staticmethod
    def post(request: Request) -> Response:
        logger.debug("POST /auth/verify-access/")
        try:
            access_payload_dto: AccessPayloadDto = gateway.auth_app_service.verify_access_from_headers(
                headers=cast(dict[str, str], request.headers)
            )
            return Response(asdict(access_payload_dto), status=status.HTTP_200_OK)
        except (DomainException, pydantic.ValidationError) as e:
            return CommonErrorResponseFactory.create_response(e)


class LogoutView(APIView):
    @staticmethod
    def post(request: Request) -> Response:
        logger.info("POST /auth/logout/")
        response = Response({"detail": SUCCESS}, status.HTTP_200_OK)
        gateway.cookie_service.remove_refresh_token_from_cookies(response=cast(CookiesResponseProtocol, response))
        return response
