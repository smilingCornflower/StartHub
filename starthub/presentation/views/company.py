from application.service_factories.company import CompanyServiceFactory
from application.services.company import CompanyAppService
from application.utils.get_access_payload_dto import get_access_payload_dto
from loguru import logger
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class CompanyView(APIView):
    @staticmethod
    def post(request: Request) -> Response:
        logger.info("Started creating a company.")

        access_dto = get_access_payload_dto(request.COOKIES)

        company_service: CompanyAppService = CompanyServiceFactory.create_service()
        company_service.create(request.data, int(access_dto.sub))

        return Response({"detail": "success"}, 201)
