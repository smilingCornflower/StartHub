from dataclasses import asdict
from typing import cast

import pydantic
from loguru import logger
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from application.dto.auth import AccessPayloadDto, AccessTokenDto, AnonymousPayloadDto, AnonymousTokenDto, TokenPairDto
from application.ports.cookie_service import CookiesResponseProtocol
from application.services.gateway import gateway
from domain.enums.token import TokenNameEnum
from domain.exceptions import DomainException
from presentation.constants import SUCCESS
from presentation.response_factories.common import (
    CommonErrorResponseFactory,
    LoginErrorResponseFactory,
    RegistrationErrorResponseFactory,
    ReissueAccessErrorResponseFactory,
)


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

        response = Response(
            data={TokenNameEnum.ACCESS_TOKEN: tokens_pair_dto.access_token, "code": SUCCESS}, status=200
        )
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
            return Response(
                {TokenNameEnum.ACCESS_TOKEN: access_token_dto.access_token, "code": SUCCESS}, status=status.HTTP_200_OK
            )
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


class GenerateAnonymousView(APIView):
    @staticmethod
    def post(request: Request) -> Response:
        logger.info("POST /auth/generate-anonymous/")
        anonymous_token_dto: AnonymousTokenDto = gateway.auth_app_service.generate_anonymous()
        return Response(
            {TokenNameEnum.ANONYMOUS_TOKEN: anonymous_token_dto.anonymous_token, "code": SUCCESS},
            status=status.HTTP_200_OK,
        )


class VerifyAnonymousView(APIView):
    @staticmethod
    def post(request: Request) -> Response:
        logger.info("POST /auth/verify-anonymous/")
        try:
            anonymous_payload_dto: AnonymousPayloadDto = gateway.auth_app_service.verify_anonymous_from_headers(
                headers=cast(dict[str, str], request.headers)
            )
            # noinspection PyTypeChecker
            return Response(asdict(anonymous_payload_dto), status=status.HTTP_200_OK)
        except (DomainException, pydantic.ValidationError) as e:
            return CommonErrorResponseFactory.create_response(e)
