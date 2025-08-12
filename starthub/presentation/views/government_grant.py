from application.services.gateway import gateway
from domain.exceptions import CustomException
from domain.value_objects.common import Id
from domain.value_objects.project.government_grant import ProjectGoverntmentGrantCreateCommand
from infrastructure.auth.user import get_user_id_or_raises
from presentation.constants import SUCCESS
from presentation.request_converters.project.government_grant import request_to_project_government_grant_create_command
from presentation.response_factories.common import ProjectGovernmentGrantErrorResponseFactory
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class GovernmentGrantView(APIView):
    def post(self, request: Request, project_id: int) -> Response:
        try:
            user_id: Id = get_user_id_or_raises(request=request)
            command: ProjectGoverntmentGrantCreateCommand = request_to_project_government_grant_create_command(
                request=request
            )
            gateway.project_government_grant_app_service.create(
                user_id=user_id, project_id=Id(value=project_id), command=command
            )

            return Response({"code": SUCCESS}, status=status.HTTP_201_CREATED)
        except CustomException as e:
            return ProjectGovernmentGrantErrorResponseFactory.create_response(exception=e)
