from application.services.gateway import gateway
from domain.exceptions import CustomException
from domain.value_objects.common import Id
from domain.value_objects.project.bank_loan import (
    ProjectBankLoanCreateCommand,
    ProjectBankLoanId,
    ProjectBankLoanUpdateCommand,
)
from presentation.constants import SUCCESS
from presentation.helpers.auth import get_authenticated_user_from_request
from presentation.request_converters.project.bank_loan import (
    request_to_bank_loan_create_command,
    request_to_bank_loan_update_command,
)
from presentation.response_factories.project_management import ProjectBankLoanErrorResponseFactory
from pydantic import ValidationError
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class ProjectBankLoanView(APIView):
    def post(self, request: Request, project_id: int) -> Response:
        try:
            user = get_authenticated_user_from_request(request=request)
            user_id = Id(value=user.id)
            command: ProjectBankLoanCreateCommand = request_to_bank_loan_create_command(request=request)
            gateway.project_bank_loan_app_service.create(
                user_id=user_id, project_id=Id(value=project_id), command=command
            )

            return Response({"code": SUCCESS}, status=status.HTTP_201_CREATED)
        except (CustomException, ValidationError) as e:
            return ProjectBankLoanErrorResponseFactory.create_response(exception=e)

    def patch(self, request: Request, bank_loan_id: int) -> Response:
        try:
            user = get_authenticated_user_from_request(request=request)
            user_id = Id(value=user.id)
            command: ProjectBankLoanUpdateCommand = request_to_bank_loan_update_command(request=request)
            gateway.project_bank_loan_app_service.update(
                user_id=user_id, bank_loan_id=ProjectBankLoanId(value=bank_loan_id), command=command
            )

            return Response({"code": SUCCESS}, status=status.HTTP_200_OK)

        except (CustomException, ValidationError) as e:
            return ProjectBankLoanErrorResponseFactory.create_response(exception=e)

    def delete(self, request: Request, bank_loan_id: int) -> Response:
        try:
            user = get_authenticated_user_from_request(request=request)
            user_id = Id(value=user.id)
            gateway.project_bank_loan_app_service.delete(
                user_id=user_id, bank_loan_id=ProjectBankLoanId(value=bank_loan_id)
            )

            return Response({"code": SUCCESS}, status=status.HTTP_200_OK)

        except (CustomException, ValidationError) as e:
            return ProjectBankLoanErrorResponseFactory.create_response(exception=e)
