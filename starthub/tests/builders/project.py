from datetime import date, timedelta

from domain.enums.project_stage import ProjectStageEnum
from domain.enums.project_status import ProjectStatusEnum
from domain.models.company import Company, CompanyFounder
from domain.models.funding_model import FundingModel
from domain.models.geo.country import Country
from domain.models.project_management.project import Project
from domain.models.project_management.category import ProjectCategory
from domain.value_objects.common import Id


def create_project_instance(user_id: Id) -> Project:
    funding_model, _ = FundingModel.objects.get_or_create(name="Funding Model")
    category_1, _ = ProjectCategory.objects.get_or_create(name="Category 1")
    category_2, _ = ProjectCategory.objects.get_or_create(name="Category 2")
    country, _ = Country.objects.get_or_create(code="KZ")
    project, _ = Project.objects.get_or_create(
        name="Project Name",
        description="Description",
        funding_model_id=funding_model.id,
        goal_sum=10_000,
        deadline=date.today() + timedelta(days=1),
        plan="plan_path",
        stage=ProjectStageEnum.MVP,
        status=ProjectStatusEnum.ACTIVE,
        creator_id=user_id.value,
    )
    project.categories.set([category_1.id, category_2.id])
    company, _ = Company.objects.get_or_create(
        name="Company",
        project_id=project.id,
        country_id=country.id,
        business_id="1" * 12,
        established_date=date.today() - timedelta(days=1),
    )
    company_founder, _ = CompanyFounder.objects.get_or_create(name="Name", surname="Surname", company_id=company.id)
    return project
