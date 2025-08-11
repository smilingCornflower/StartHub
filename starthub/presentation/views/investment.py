from application.services.gateway import gateway
from domain.exceptions import CustomException
from domain.value_objects.common import Id
from domain.value_objects.project.investment import ProjectInvestmentId
from domain.value_objects.project.project_investment_social_link import ProjectInvestmentSocialLinkId
from infrastructure.auth.user import get_user_id_or_raises
from presentation.constants import SUCCESS
from presentation.request_converters.project.investment import (
    request_to_project_investment_create_command,
    request_to_project_investment_update_command,
    request_to_social_link,
)
from presentation.response_factories.common import ProjectInvestmentErrorResponseFactory
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class ProjectInvestmentView(APIView):
    def post(self, request: Request, project_id: int) -> Response:
        try:
            user_id: Id = get_user_id_or_raises(request=request)
            command = request_to_project_investment_create_command(request=request)
            gateway.project_investment_app_service.create(
                user_id=user_id, project_id=Id(value=project_id), command=command
            )

            return Response({"code": SUCCESS}, status=status.HTTP_201_CREATED)
        except CustomException as e:
            return ProjectInvestmentErrorResponseFactory.create_response(exception=e)

    def patch(self, request: Request, project_id: int, investment_id: int) -> Response:
        try:
            user_id: Id = get_user_id_or_raises(request=request)
            command = request_to_project_investment_update_command(request=request)
            gateway.project_investment_app_service.update(
                user_id=user_id,
                project_id=Id(value=project_id),
                investment_id=ProjectInvestmentId(value=investment_id),
                command=command,
            )
            return Response({"code": SUCCESS}, status=status.HTTP_200_OK)
        except CustomException as e:
            return ProjectInvestmentErrorResponseFactory.create_response(exception=e)


class ProjectInvestmentSocialLinkView(APIView):
    def post(self, request: Request, investment_id: int) -> Response:
        try:
            user_id: Id = get_user_id_or_raises(request=request)
            social_links = request_to_social_link(request=request)
            gateway.project_investment_social_link_app_service.create(
                user_id=user_id,
                investment_id=ProjectInvestmentId(value=investment_id),
                social_links=social_links,
            )
            return Response({"code": SUCCESS}, status=status.HTTP_201_CREATED)
        except CustomException as e:
            return ProjectInvestmentErrorResponseFactory.create_response(exception=e)

    def delete(self, request: Request, social_link_id: int) -> Response:
        try:
            user_id: Id = get_user_id_or_raises(request=request)
            gateway.project_investment_social_link_app_service.delete(
                user_id=user_id, social_link_id=ProjectInvestmentSocialLinkId(value=social_link_id)
            )

            return Response({"code": SUCCESS}, status=status.HTTP_200_OK)
        except CustomException as e:
            return ProjectInvestmentErrorResponseFactory.create_response(exception=e)
