from domain.models.company import Company
from domain.repositories.company import CompanyWriteRepository
from domain.repositories.user import UserReadRepository
from domain.value_objects.company import CompanyCreatePayload


class CompanyService:
    def __init__(self, company_write_repository: CompanyWriteRepository, user_read_repository: UserReadRepository):
        self._company_write_repository = company_write_repository
        self._user_read_repository = user_read_repository

    def create(self, payload: CompanyCreatePayload) -> Company:
        """:raises UserNotFoundException:"""

        self._user_read_repository.get_by_id(id_=payload.representative_id)
        return self._company_write_repository.create(payload)
