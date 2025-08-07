from domain.constants import PROJECT_STEPS_MAX_AMOUNT
from domain.exceptions.project_management import ProjectStepMaxAmountException
from domain.models.project_management.project import Project
from domain.models.project_management.step import ProjectStep
from domain.ports.service import AbstractDomainService
from domain.repositories.project.step import ProjectStepReadRepository, ProjectStepWriteRepository
from domain.value_objects.common import Id
from domain.value_objects.filter import ProjectStepFilter
from domain.value_objects.project.step import ProjectStepCreateCommand, ProjectStepCreatePaylaod, ProjectStepId
from loguru import logger


class ProjectStepService(AbstractDomainService):
    def __init__(
        self,
        read_repository: ProjectStepReadRepository,
        write_repository: ProjectStepWriteRepository,
    ):
        self._read_repository = read_repository
        self._write_repository = write_repository

    def create(self, paylaod: ProjectStepCreatePaylaod) -> ProjectStep:
        project_step: ProjectStep = self._write_repository.create(data=paylaod)
        return project_step

    def delete(self, step: ProjectStep) -> None:
        self._write_repository.delete_by_id(id_=ProjectStepId(value=step.id))

    def delete_all_for_project(self, project: Project) -> None:
        project_steps = self._read_repository.get_all(filter_=ProjectStepFilter(project_id=Id(value=project.id)))
        for step in project_steps:
            self.delete(step=step)
        logger.info("All steps deleted successfully.")

    @staticmethod
    def check_project_max_steps_limit(project_steps: list[ProjectStepCreateCommand]) -> None:
        logger.debug(f"{project_steps=}")

        if len(project_steps) > PROJECT_STEPS_MAX_AMOUNT:
            logger.exception("Project step limit exceeded: max allowed is {PROJECT_STEPS_MAX_AMOUNT}")
            raise ProjectStepMaxAmountException(
                "Project step limit exceeded: max allowed is {PROJECT_STEPS_MAX_AMOUNT}"
            )

        logger.debug(f"Project steps count is {len(project_steps)}, within allowed limit")
