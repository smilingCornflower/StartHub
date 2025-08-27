from dataclasses import asdict

from application.dto.project import CategoryDto, FundingModelDto
from domain.models.project_management.category import ProjectCategory
from domain.models.project_management.funding_model import FundingModel
from loguru import logger
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
            FundingModelDto(id=i.id, name=i.name, slug=i.slug) for i in FundingModel.objects.all()
        ]
        return Response(list(map(asdict, funding_models)), status=status.HTTP_200_OK)


class ProjectCategoryView(APIView):
    @staticmethod
    def get(request: Request) -> Response:
        print()
        logger.info(f"{request.method} {request.path}")

        categories: list[CategoryDto] = [
            CategoryDto(id=i.id, name=i.name, slug=i.slug) for i in ProjectCategory.objects.all()
        ]
        return Response(list(map(asdict, categories)), status=status.HTTP_200_OK)
