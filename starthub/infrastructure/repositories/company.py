from domain.exceptions.company import CompanyNotFoundException
from domain.models.company import Company
from domain.repositories.company import CompanyReadRepository, CompanyWriteRepository
from domain.value_objects.common import Id
from domain.value_objects.company import CompanyCreatePayload, CompanyUpdatePayload
from domain.value_objects.filter import CompanyFilter


class DjCompanyReadRepository(CompanyReadRepository):
    def get_by_id(self, id_: Id) -> Company:
        company: Company | None = Company.objects.filter(id=id_.value).first()
        if company is None:
            raise CompanyNotFoundException(f"Company with id = {id_.value} does not exist.")
        return company

    def get_all(self, filter_: CompanyFilter) -> list[Company]:
        return list(Company.objects.all())


class DjCompanyWriteRepository(CompanyWriteRepository):
    def create(self, data: CompanyCreatePayload) -> Company:
        return Company.objects.create(
            name=data.name,
            representative_id=data.representative_id.value,
            country_id=data.country_id.value,
            business_id=data.business_id.value,
            established_date=data.established_date,
            description=data.description,
        )

    def update(self, data: CompanyUpdatePayload) -> Company:
        raise NotImplementedError("Method update() is not implemented yet.")

    def delete(self, id_: Id) -> None:
        raise NotImplementedError("Method delete() is not implemented yet.")
