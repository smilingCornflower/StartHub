from django.db.models import QuerySet
from domain.exceptions.company import CompanyNotFoundException
from domain.models.company import Company, CompanyFounder
from domain.repositories.company import CompanyFounderWriteRepository, CompanyReadRepository, CompanyWriteRepository
from domain.value_objects.common import Id
from domain.value_objects.company import (
    CompanyCreatePayload,
    CompanyFounderCreatePayload,
    CompanyFounderUpdatePayload,
    CompanyUpdatePayload,
)
from domain.value_objects.filter import CompanyFilter


class DjCompanyReadRepository(CompanyReadRepository):
    def get_by_id(self, id_: Id) -> Company:
        """:raises CompanyNotFoundException:"""
        company: Company | None = Company.objects.filter(id=id_.value).first()
        if company is None:
            raise CompanyNotFoundException(f"Company with id = {id_.value} does not exist.")
        return company

    def get_all(self, filter_: CompanyFilter) -> list[Company]:
        queryset: QuerySet[Company] = Company.objects.all()

        if filter_.business_id:
            queryset = queryset.filter(business_id=filter_.business_id.value)
        return list(queryset.distinct())

    def get_by_project_id(self, id_: Id) -> Company:
        """:raises CompanyNotFoundException:"""
        company: Company | None = Company.objects.filter(project__id=id_.value).first()
        if company is None:
            raise CompanyNotFoundException(f"Company with project id = {id_.value} does not exist.")
        return company


class DjCompanyWriteRepository(CompanyWriteRepository):
    def create(self, data: CompanyCreatePayload) -> Company:
        return Company.objects.create(
            name=data.name,
            representative_id=data.representative_id.value,
            country_id=data.country_id.value,
            founder_id=data.founder_id.value,
            business_id=data.business_id.value,
            established_date=data.established_date,
            description=data.description,
        )

    def update(self, data: CompanyUpdatePayload) -> Company:
        """:raises CompanyNotFoundException:"""
        company: Company | None = Company.objects.filter(project__id=data.project_id.value).first()
        if company is None:
            raise CompanyNotFoundException(f"Company with project id = {data.project_id.value} does not exist.")

        if data.name is not None:
            company.name = data.name
            company.slug = None
        if data.description is not None:
            company.description = data.description
        if data.established_date is not None:
            company.established_date = data.established_date

        company.save()
        return company

    def delete(self, id_: Id) -> None:
        """:raises NotImplementedError:"""
        raise NotImplementedError("Method delete() is not implemented yet.")


class DjCompanyFounderWriteRepository(CompanyFounderWriteRepository):
    def create(self, data: CompanyFounderCreatePayload) -> CompanyFounder:
        return CompanyFounder.objects.create(
            name=data.name.value, surname=data.surname.value, description=data.description
        )

    def update(self, data: CompanyFounderUpdatePayload) -> CompanyFounder:
        raise NotImplementedError("The method update() is not implemented yet.")

    def delete(self, id_: Id) -> None:
        raise NotImplementedError("The method delete() is not implemented yet.")
