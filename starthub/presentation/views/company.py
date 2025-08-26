from dataclasses import asdict

from application.dto.project import CompanyFullDto
from application.services.gateway import gateway
from domain.exceptions import CustomException
from domain.value_objects.common import Id
from domain.value_objects.company import CompanyUpdateCommand
from domain.value_objects.filter import CompanyFilter
from infrastructure.auth.user import get_user_id_or_raises
from loguru import logger
from presentation.constants import SUCCESS
from presentation.request_converters.common import request_to_pagination
from presentation.request_converters.company import request_to_company_update_command
from presentation.response_factories.project_management import CompanyErrorResponseFactory
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class CompanyView(APIView):
    def get(self, request: Request, company_id: int | None = None) -> Response:
        try:
            if company_id:
                company: CompanyFullDto = gateway.company_app_service.get_by_id(company_id=Id(value=company_id))
                return Response(asdict(company), status=status.HTTP_200_OK)
            else:
                pagination = request_to_pagination(request=request)
                companies: list[CompanyFullDto] = gateway.company_app_service.get(
                    filter_=CompanyFilter(), pagination=pagination
                )
                return Response(list(map(asdict, companies)), status=status.HTTP_200_OK)
        except CustomException as e:
            return CompanyErrorResponseFactory.create_response(exception=e)

    def patch(self, request: Request, company_id: int) -> Response:
        print()
        logger.info(f"PATCH /companies/{company_id}/")
        logger.debug(f"request.data = {request.data}")

        try:
            user_id: Id = get_user_id_or_raises(request=request)
            company_update_command: CompanyUpdateCommand = request_to_company_update_command(
                request=request, company_id=company_id
            )
            logger.debug(f"command = {company_update_command}")

            gateway.company_app_service.update(command=company_update_command, user_id=user_id)

            return Response({"code": SUCCESS}, status=status.HTTP_200_OK)
        except CustomException as e:
            return CompanyErrorResponseFactory.create_response(exception=e)
