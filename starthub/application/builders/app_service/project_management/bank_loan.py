from application.builders.domain_service.project_management import ProjectBankLoanServiceBuilder
from application.ports.app_service_builder import AbstractAppServiceBuilder
from application.services.project_management.bank_loan import ProjectBankLoanAppService
from infrastructure.repositories.project.bank_loan import DjProjectBankLoanReadRepository
from infrastructure.repositories.project.project import DjProjectReadRepository
from infrastructure.repositories.user_management.user import DjUserReadRepository


class ProjectBankLoanAppServiceBuilder(AbstractAppServiceBuilder[ProjectBankLoanAppService]):
    @staticmethod
    def create_service() -> ProjectBankLoanAppService:
        return ProjectBankLoanAppService(
            bank_loan_service=ProjectBankLoanServiceBuilder.create_service(),
            bank_loan_read_repository=DjProjectBankLoanReadRepository(),
            user_read_repository=DjUserReadRepository(),
            project_read_repository=DjProjectReadRepository(),
        )
