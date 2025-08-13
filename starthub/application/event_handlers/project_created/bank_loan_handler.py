from application.services.project_management.bank_loan import ProjectBankLoanAppService
from domain.events.project import ProjectCreatedEvent
from domain.ports.event import AbstractEventHandler


class ProjectCreatedBankLoanHandler(AbstractEventHandler[ProjectCreatedEvent]):
    def __init__(self, bank_loan_app_service: ProjectBankLoanAppService):
        self._bank_loan_app_service = bank_loan_app_service

    def handle(self, event: ProjectCreatedEvent) -> None:
        command = event.command
        user_id = event.user_id
        project_id = event.project_id

        if command.bank_loan is not None:
            self._bank_loan_app_service.create(user_id=user_id, project_id=project_id, command=command.bank_loan)
