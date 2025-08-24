from application.ports.service import AbstractAppService
from domain.constants import PROJECT_INVESTMENTS_PHONE_MAX_AMOUNT
from domain.exceptions.project_management import (
    ProjectInvestmentPhoneAlreadyExistsException,
    ProjectInvestmentPhoneMaxAmountException,
    ProjectInvestmentPhoneNotFoundException,
)
from domain.models.project_management.investment import ProjectInvestment, ProjectInvestmentPhone
from domain.models.project_management.project import Project
from domain.models.user_management.user import User
from domain.repositories.project.investment import ProjectInvestmentPhoneReadRepository, ProjectInvestmentReadRepository
from domain.repositories.project.project import ProjectReadRepository
from domain.repositories.user_management.user import UserReadRepository
from domain.services.project_management.investment import ProjectInvestmentPhoneService
from domain.value_objects.common import Id, PhoneNumber
from domain.value_objects.filter import ProjectInvestmentPhoneFilter
from domain.value_objects.project.investment import ProjectInvestmentId
from domain.value_objects.project.project_investment_phone import ProjectInvestmentPhoneCreatePayload


class ProjectInvestmentPhoneAppService(AbstractAppService):
    def __init__(
        self,
        project_investment_phone_service: ProjectInvestmentPhoneService,
        project_investment_phone_read_repository: ProjectInvestmentPhoneReadRepository,
        investment_read_repository: ProjectInvestmentReadRepository,
        project_read_repository: ProjectReadRepository,
        user_read_repository: UserReadRepository,
    ):
        self._project_investment_phone_service = project_investment_phone_service
        self._project_investment_phone_read_repository = project_investment_phone_read_repository
        self._investment_read_repository = investment_read_repository
        self._project_read_repository = project_read_repository
        self._user_read_repository = user_read_repository

    def create(self, user_id: Id, investment_id: ProjectInvestmentId, phone_number: PhoneNumber) -> None:
        """
        :raises UserNotFounException:
        :raises ProjectInvestmentNotFoundException:
        :raises ProjectInvestmentPhoneAlreadyExistsException:
        """
        self._check_max_amount(investment_id=investment_id)
        self._check_dublicate_number(number=phone_number)

        user: User = self._user_read_repository.get_by_id(id_=user_id)
        investment: ProjectInvestment = self._investment_read_repository.get_by_id(id_=investment_id)
        project: Project = self._project_read_repository.get_by_id(id_=Id(value=investment.project_id))

        self._project_investment_phone_service.create(
            user=user,
            project=project,
            payload=ProjectInvestmentPhoneCreatePayload(
                investment_id=ProjectInvestmentId(value=investment.id), phone_number=phone_number
            ),
        )

    def _check_max_amount(self, investment_id: ProjectInvestmentId) -> None:
        """:raises ProjectInvestmentPhoneMaxAmountException:"""
        phones: list[ProjectInvestment] = self._project_investment_phone_read_repository.get_all(
            filter_=ProjectInvestmentPhoneFilter(investment_id=investment_id)
        )
        if not (len(phones) < PROJECT_INVESTMENTS_PHONE_MAX_AMOUNT):
            raise ProjectInvestmentPhoneMaxAmountException(
                f"Maximum number of phones ({PROJECT_INVESTMENTS_PHONE_MAX_AMOUNT}) for investment {investment_id} has been reached"
            )
        return None

    def _check_dublicate_number(self, number: PhoneNumber) -> None:
        """:raises ProjectInvestmentPhoneAlreadyExistsException:"""
        phones = self._project_investment_phone_read_repository.get_all(
            filter_=ProjectInvestmentPhoneFilter(number=number)
        )
        if phones:
            raise ProjectInvestmentPhoneAlreadyExistsException("This number already exists for this investment.")

    def delete(self, user_id: Id, investment_id: ProjectInvestmentId, phone_number: PhoneNumber) -> None:
        """:raises ProjectInvestmentPhoneNotFoundException:"""

        user: User = self._user_read_repository.get_by_id(id_=user_id)
        investment: ProjectInvestment = self._investment_read_repository.get_by_id(id_=investment_id)
        project: Project = self._project_read_repository.get_by_id(id_=Id(value=investment.project_id))

        investment_phones: list[ProjectInvestmentPhone] = self._project_investment_phone_read_repository.get_all(
            filter_=ProjectInvestmentPhoneFilter(number=phone_number)
        )
        if investment_phones:
            self._project_investment_phone_service.delete(user=user, project=project, phone_number=investment_phones[0])
        else:
            raise ProjectInvestmentPhoneNotFoundException(
                f"Phone number {phone_number.value} for the investment {investment.organization_name} does not exist."
            )
