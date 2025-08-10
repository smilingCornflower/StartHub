from rest_framework.views import APIView
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response

from application.services.gateway import gateway
from domain.exceptions import CustomException
from infrastructure.auth.user import get_user_id_or_raises
from presentation.constants import SUCCESS
from presentation.response_factories.common import CrowdfundingErrorResponseFactory
from domain.value_objects.common import Id
from domain.value_objects.project.crowdfunding import ProjectCrowdfundingId


class CrowdfundingView(APIView):
    def delete(self, request: Request, crowdfunding_id: int) -> Response:
        try:
            user_id: Id = get_user_id_or_raises(request=request)
            gateway.crowdfunding_app_service.delete(user_id=user_id, crowdfunding_id=ProjectCrowdfundingId(value=crowdfunding_id))
            return Response({"code": SUCCESS}, status=status.HTTP_200_OK)
        except CustomException as e:
            return CrowdfundingErrorResponseFactory.create_response(e)