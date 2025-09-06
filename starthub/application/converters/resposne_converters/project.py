from application.dto.project import CategoryDto, CompanyDto, CompanyFounderDto, FundingModelDto, ProjectDto
from application.dto.user import UserDto
from domain.models.project_management.category import ProjectCategory
from domain.models.project_management.project import Project
from domain.models.user_management.user import User


def project_to_dto(
    project: Project,
    categories: list[ProjectCategory],
    media_links: list[str | None] | None = None,
    is_favorite: bool = False,
) -> ProjectDto:
    creater: User = project.creator
    return ProjectDto(
        id=project.id,
        name=project.name,
        slug=project.slug,
        user=UserDto(id=creater.id, first_name=creater.first_name, last_name=creater.last_name, email=creater.email),
        goal_descriptioin=project.goal_description,
        description=project.description,
        company=CompanyDto(
            id=project.company.id,
            name=project.company.name,
            slug=project.company.slug,
            country_code=project.company.country.code,
            business_id=project.company.business_id,
            established_date=project.company.established_date,
            founder=CompanyFounderDto(
                name=project.company.founder.name,
                surname=project.company.founder.surname,
                description=project.company.founder.description,
            ),
        ),
        media=list() if media_links is None else media_links,
        categories=[
            CategoryDto(
                id=category.id,
                name=category.name,
                slug=category.slug,
            )
            for category in categories
        ],
        funding_model=FundingModelDto(
            id=project.funding_model.id,
            name=project.funding_model.name,
            slug=project.funding_model.slug,
            recommended=project.funding_model.recommended,
            description=project.funding_model.description,
        ),
        stage=project.stage.name,
        status=project.status,
        goal_sum=float(project.goal_sum),
        current_sum=float(project.current_sum),
        deadline=project.deadline,
        is_favorite=is_favorite,
    )
