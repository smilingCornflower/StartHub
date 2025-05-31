from django.db.models import Q, QuerySet
from domain.exceptions.project_phone import ProjectPhoneAlreadyExistsException, ProjectPhoneNotFoundException
from domain.models.project import ProjectPhone
from domain.repositories.project_phone import ProjectPhoneReadRepository, ProjectPhoneWriteRepository
from domain.value_objects.common import Id
from domain.value_objects.filter import ProjectPhoneFilter
from domain.value_objects.project_phone import ProjectPhoneCreatePayload, ProjectPhoneUpdatePayload


class DjProjectPhoneReadRepository(ProjectPhoneReadRepository):
    def get_by_id(self, id_: Id) -> ProjectPhone:
        """:raises ProjectPhoneNotFoundException:"""
        project_phone: ProjectPhone | None = ProjectPhone.objects.filter(id=id_.value).first()
        if project_phone is None:
            raise ProjectPhoneNotFoundException(f"Project phone with id = {id_.value} not found.")
        return project_phone

    def get_all(self, filter_: ProjectPhoneFilter) -> list[ProjectPhone]:
        queryset: QuerySet[ProjectPhone] = ProjectPhone.objects.all()
        if filter_.project_id:
            queryset = queryset.filter(project_id=filter_.project_id.value)
        if filter_.number:
            queryset = queryset.filter(number=filter_.number.value)
        return list(queryset.distinct())


class DjProjectPhoneWriteRepository(ProjectPhoneWriteRepository):
    def create(self, data: ProjectPhoneCreatePayload) -> ProjectPhone:
        """:raises ProjectPhoneAlreadyExistsException:"""
        if ProjectPhone.objects.filter(Q(project_id=data.project_id.value) & Q(number=data.number.value)).exists():
            raise ProjectPhoneAlreadyExistsException(
                f"For the project with id = {data.project_id.value} this number already exists."
            )

        return ProjectPhone.objects.create(project_id=data.project_id.value, number=data.number.value)

    def update(self, data: ProjectPhoneUpdatePayload) -> ProjectPhone:
        """:raises ProjectPhoneNotFoundException:"""
        project_phone: ProjectPhone | None = ProjectPhone.objects.filter(id=data.phone_id.value).first()
        if project_phone is None:
            raise ProjectPhoneNotFoundException(f"Project phone with id = {data.phone_id} not found.")
        project_phone.number = data.number.value
        project_phone.save()
        return project_phone

    def delete(self, id_: Id) -> None:
        """:raises ProjectPhoneNotFoundException:"""
        try:
            ProjectPhone.objects.get(id=id_.value).delete()
        except ProjectPhone.DoesNotExist:
            raise ProjectPhoneNotFoundException(f"Project phone with id = {id_.value} not found.")
