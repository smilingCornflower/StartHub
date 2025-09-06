from dataclasses import asdict

import pydantic
from application.dto.project import FundingModelDto
from application.services.gateway import gateway
from domain.exceptions import CustomException
from domain.models.project_management.funding_model import FundingModel
from domain.value_objects.common import Id
from domain.value_objects.project.funding_model import FundingModelId, FundingModelUpdateCommand
from loguru import logger
from presentation.constants import SUCCESS
from presentation.helpers.auth import get_authenticated_user_from_request
from presentation.request_converters.others import FundingModelErrorResponseFactory
from presentation.request_converters.project.funding_model import request_to_funding_model_update_command
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class FundingModelView(APIView):
    @staticmethod
    def get(request: Request) -> Response:
        print()
        logger.info(f"{request.method} {request.path}")

        funding_models: list[FundingModelDto] = [
            FundingModelDto(id=i.id, name=i.name, slug=i.slug, description=i.description, recommended=i.recommended)
            for i in FundingModel.objects.all()
        ]
        return Response(list(map(asdict, funding_models)), status=status.HTTP_200_OK)

    @staticmethod
    def patch(request: Request, funding_model_id: int) -> Response:
        print()
        logger.info(f"{request.method} {request.path}")
        try:
            user = get_authenticated_user_from_request(request=request)
            user_id = Id(value=user.id)
            command: FundingModelUpdateCommand = request_to_funding_model_update_command(request=request)
            gateway.funding_model_app_service.update(
                user_id=user_id, funding_model_id=FundingModelId(value=funding_model_id), command=command
            )
            return Response({"code": SUCCESS}, status=status.HTTP_200_OK)
        except (CustomException, pydantic.ValidationError) as e:
            return FundingModelErrorResponseFactory.create_response(exception=e)
