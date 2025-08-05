from domain.enums.permission import ActionEnum, ScopeEnum
from domain.exceptions.company import BusinessNumberAlreadyExistsException, CompanyFounderAlreadyExistsException
from domain.exceptions.geo.country import CountryNotFoundException
from domain.exceptions.permissions import UpdateDeniedPermissionException
from domain.models.company import Company, CompanyFounder
from domain.models.geo.country import Country
from domain.models.user import User
from domain.ports.service import AbstractDomainService
from domain.repositories.company import (
    CompanyFounderReadRepository,
    CompanyFounderWriteRepository,
    CompanyReadRepository,
    CompanyWriteRepository,
)
from domain.repositories.country import CountryReadRepository
from domain.repositories.geo.address import AddressWriteRepository
from domain.services.permission import PermissionService
from domain.value_objects.common import Id
from domain.value_objects.company import (
    CompanyCreateCommand,
    CompanyCreatePayload,
    CompanyFounderCreatePayload,
    CompanyUpdatePayload,
)
from domain.value_objects.filter import CompanyFilter, CompanyFounderFilter, CountryFilter
from domain.value_objects.user import PermissionVo
from loguru import logger


class CompanyService(AbstractDomainService):
    def __init__(
        self,
        company_read_repository: CompanyReadRepository,
        country_read_repository: CountryReadRepository,
        company_write_repository: CompanyWriteRepository,
        address_write_repository: AddressWriteRepository,
        permission_service: PermissionService,
    ):
        self._company_read_repository = company_read_repository
        self._country_read_repository = country_read_repository
        self._company_write_repository = company_write_repository
        self._address_write_repository = address_write_repository
        self._permission_service = permission_service

    def create(self, command: CompanyCreateCommand) -> Company:
        """
        :raises CountryNotFoundException:
        :raises UserNotFoundException:
        :raises BusinessNumberAlreadyExistsException:
        """
        search_result: list[Company] = self._company_read_repository.get_all(
            CompanyFilter(business_id=command.business_id)
        )
        if search_result:
            raise BusinessNumberAlreadyExistsException("This business number already exists.")

        countries: list[Country] = self._country_read_repository.get_all(CountryFilter(code=command.country_code))
        if not countries:
            raise CountryNotFoundException(f"A country with code = {command.country_code.value} not found.")
        country: Country = countries[0]

        return self._company_write_repository.create(
            CompanyCreatePayload(
                name=command.name,
                project_id=command.project_id,
                country_id=Id(value=country.id),
                business_id=command.business_id,
                established_date=command.established_date,
                description=command.description,
                address_id=command.address_id,
            )
        )

    def update(self, company: Company, payload: CompanyUpdatePayload, user: User) -> None:
        self._check_update_permissions(user=user, company=company)
        self._company_write_repository.update(data=payload)
        logger.info(f"Company with id = {company.id} update successfully.")

    def _check_update_permissions(self, user: User, company: Company) -> None:
        if self._has_update_all_permission(user=user):
            return

        change_own_permission: PermissionVo = self._permission_service.create_permission_vo(
            model=Company, action=ActionEnum.CHANGE, scope=ScopeEnum.OWN
        )
        has_permission: bool = self._permission_service.has_user_permission(
            user=user, permission_vo=change_own_permission
        )
        logger.debug(f"{has_permission=}")

        if has_permission:
            if company.project.creator == user:
                logger.debug("User has enough permissions to update the company.")
                return

        logger.exception(f"User {user} does not have enough permissions to update the company {company}.")
        raise UpdateDeniedPermissionException("You don't have enough permissions to update this company.")

    def _has_update_all_permission(self, user: User) -> bool:
        change_any_permission: PermissionVo = self._permission_service.create_permission_vo(
            model=Company, action=ActionEnum.CHANGE, scope=ScopeEnum.ANY
        )
        has_permission: bool = self._permission_service.has_user_permission(
            user=user, permission_vo=change_any_permission
        )
        return has_permission


class CompanyFounderService(AbstractDomainService):
    def __init__(
        self,
        company_founder_write_repository: CompanyFounderWriteRepository,
        company_founder_read_repository: CompanyFounderReadRepository,
    ):
        self._company_founder_write_repository = company_founder_write_repository
        self._company_founder_read_repository = company_founder_read_repository

    def create(self, payload: CompanyFounderCreatePayload) -> CompanyFounder:
        search_result: list[CompanyFounder] = self._company_founder_read_repository.get_all(
            filter_=CompanyFounderFilter(company_id=payload.company_id)
        )
        if search_result:
            raise CompanyFounderAlreadyExistsException(
                f"Company founder for the company with id = {payload.company_id.value} already exists."
            )

        return self._company_founder_write_repository.create(payload)
