from application.dto.project import CategoryDto, CompanyDto, CompanyFounderDto, FundingModelDto, ProjectDto
from domain.models.project import Project


def project_to_dto(project: Project, image_links: list[str] | None = None) -> ProjectDto:
    return ProjectDto(
        id=project.id,
        name=project.name,
        slug=project.slug,
        description=project.description,
        creator_id=project.creator.id,
        company=CompanyDto(
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
        images=list() if image_links is None else image_links,
        category=CategoryDto(
            id=project.category.id,
            name=project.category.name,
            slug=project.category.slug,
        ),
        funding_model=FundingModelDto(
            id=project.funding_model.id,
            name=project.funding_model.name,
            slug=project.funding_model.slug,
        ),
        stage=project.stage,
        goal_sum=float(project.goal_sum),
        current_sum=float(project.current_sum),
        deadline=project.deadline,
    )


def projects_to_dtos(projects: list[Project]) -> list[ProjectDto]:
    return [project_to_dto(project) for project in projects]
