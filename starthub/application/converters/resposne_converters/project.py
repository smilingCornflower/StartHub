from application.dto.project import CategoryDto, FundingModelDto, ProjectDto
from domain.models.project import Project


def project_to_dto(project: Project) -> ProjectDto:
    return ProjectDto(
        id=project.id,
        name=project.name,
        slug=project.slug,
        description=project.description,
        creator_id=project.creator.id,
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
        goal_sum=float(project.goal_sum),
        current_sum=float(project.current_sum),
        deadline=project.deadline,
    )


def projects_to_dtos(projects: list[Project]) -> list[ProjectDto]:
    return [project_to_dto(project) for project in projects]
