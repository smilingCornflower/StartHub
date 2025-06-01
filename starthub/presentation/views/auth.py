from dataclasses import asdict

from application.dto.auth import AccessPayloadDto, AccessTokenDto, TokenPairDto
from application.service_factories.auth import AuthServiceFactory, RegistrationServiceFactory
from application.services.auth import AuthAppService, RegistrationAppService
from domain.exceptions.auth import InvalidCredentialsException, InvalidTokenException
from domain.exceptions.user import EmailAlreadyExistsException, UsernameAlreadyExistsException
from domain.exceptions.validation import ValidationException
from loguru import logger
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class LoginView(APIView):
    parser_classes = [JSONParser]

    @staticmethod
    def post(request: Request) -> Response:
        form_data: dict[str, str] = request.data
        logger.debug(f"request data = {form_data}")

        auth_service: AuthAppService = AuthServiceFactory.create_service()
        try:
            tokens_pair_dto: TokenPairDto = auth_service.login(form_data)
        except (InvalidCredentialsException, ValidationException) as e:
            logger.error(e)
            return Response({"detail": str(e)}, status.HTTP_400_BAD_REQUEST)

        response = Response(data={"detail": "success"}, status=200)
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

    @staticmethod
    def post(request: Request) -> Response:
        form_data: dict[str, str] = request.data
        registration_service: RegistrationAppService = RegistrationServiceFactory.create_service()
        try:
            registration_service.register(form_data)
        except (
            ValidationException,
            UsernameAlreadyExistsException,
            EmailAlreadyExistsException,
        ) as e:
            logger.error(e)
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"detail": "User has registered successfully."}, status.HTTP_201_CREATED)


class ReissueAccessTokenView(APIView):
    parser_classes = [JSONParser]

    @staticmethod
    def post(request: Request) -> Response:
        auth_service: AuthAppService = AuthServiceFactory.create_service()

        try:
            access_token_dto: AccessTokenDto = auth_service.reissue_access(request.COOKIES)
        except (ValidationException, InvalidTokenException) as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        response = Response(data={"detail": "success"}, status=200)
        response.set_cookie(
            "access_token",
            access_token_dto.access_token,
            httponly=False,
            samesite="None",
            secure=True,
        )
        return response


class AccessVerifyView(APIView):

    @staticmethod
    def post(request: Request) -> Response:
        auth_service: AuthAppService = AuthServiceFactory.create_service()

        try:
            access_payload_dto: AccessPayloadDto = auth_service.verify_access(request.COOKIES)
        except (ValidationException, InvalidTokenException) as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(asdict(access_payload_dto), status=status.HTTP_200_OK)
