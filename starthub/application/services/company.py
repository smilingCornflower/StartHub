from loguru import logger

from application.converters.resposne_converters.company import company_to_dto
from application.dto.project import CompanyFullDto
from application.ports.service import AbstractAppService
from domain.models.company import Company
from domain.models.geo.address import Address
from domain.models.user import User
from domain.repositories.company import CompanyReadRepository
from domain.repositories.geo.address import AddressWriteRepository
from domain.repositories.user import UserReadRepository
from domain.services.address import AddressService
from domain.services.company import CompanyService
from domain.value_objects.common import Id, Pagination
from domain.value_objects.company import CompanyUpdateCommand, CompanyUpdatePayload
from domain.value_objects.filter import CompanyFilter
from domain.value_objects.geo import AddressId


class CompanyAppService(AbstractAppService):
    def __init__(
        self,
        company_service: CompanyService,
        address_service: AddressService,
        company_read_repository: CompanyReadRepository,
        user_read_repository: UserReadRepository,
        address_write_repository: AddressWriteRepository,
    ):
        self._company_service = company_service
        self._address_service = address_service
        self._company_read_repository = company_read_repository
        self._user_read_repository = user_read_repository
        self._address_write_repository = address_write_repository

    def get(self, filter_: CompanyFilter, pagination: Pagination) -> list[CompanyFullDto]:
        compaies: list[Company] = self._company_read_repository.get_all(filter_=filter_, pagination=pagination)
        return [company_to_dto(company=i) for i in compaies]

    def get_by_id(self, company_id: Id) -> CompanyFullDto:
        """:raises CompanyNotFoundException:"""

        company: Company = self._company_read_repository.get_by_id(id_=company_id)
        return company_to_dto(company=company)

    def update(self, command: CompanyUpdateCommand, user_id: Id) -> None:
        company: Company = self._company_read_repository.get_by_id(id_=command.company_id)
        user: User = self._user_read_repository.get_by_id(id_=user_id)
        logger.debug("company and user found.")

        address_id: AddressId | None = None
        if command.address_create_command:
            address: Address = self._address_service.create(command=command.address_create_command)
            address_id = AddressId(value=address.id)
            logger.debug(f"address_id = {address_id}")

        payload = self._convert_update_command_to_update_payload(command=command, address_id=address_id)
        self._company_service.update(company=company, payload=payload, user=user)

    def _convert_update_command_to_update_payload(
        self, command: CompanyUpdateCommand, address_id: AddressId | None = None
    ) -> CompanyUpdatePayload:
        return CompanyUpdatePayload(
            company_id=command.company_id,
            name=command.name,
            description=command.description,
            established_date=command.established_date,
            address_id=address_id,
            patent_number=command.patent_number,
        )
