from loguru import logger

from application.ports.service import AbstractAppService
from domain.exceptions.project_management import ProjectAcceleratorAlreadyExists, ProjectAcceleratorNotFoundException
from domain.models.project_management.accelerator import ProjectAccelerator
from domain.models.project_management.project import Project
from domain.models.user import User
from domain.repositories.project.accelerator import ProjectAcceleratorReadRepository
from domain.repositories.project.project import ProjectReadRepository
from domain.repositories.user import UserReadRepository
from domain.services.project_management.accelerator import ProjectAcceleratorService
from domain.value_objects.common import Id
from domain.value_objects.filter import ProjectAcceleratorFilter
from domain.value_objects.project.accelerator import (
    ProjectAcceleratorCreateCommand,
    ProjectAcceleratorCreatePayload,
    ProjectAcceleratorUpdateCommand,
    ProjectAcceleratorUpdatePayload,
)


class AcceleratorAppService(AbstractAppService):
    def __init__(
        self,
        accelerator_service: ProjectAcceleratorService,
        accelerator_read_repository: ProjectAcceleratorReadRepository,
        user_read_repository: UserReadRepository,
        project_read_repository: ProjectReadRepository,
    ):
        self._accelerator_service = accelerator_service
        self._accelerator_read_repository = accelerator_read_repository
        self._user_read_repository = user_read_repository
        self._project_read_repository = project_read_repository

    def create(self, user_id: Id, project_id: Id, command: ProjectAcceleratorCreateCommand) -> None:
        """
        :raises ProjectAcceleratorAlreadyExists:
        :raises UserNotFoundException:
        :raises ProjectNotFoundException:
        """
        accelerators: list[ProjectAccelerator] = self._accelerator_read_repository.get_all(
            filter_=ProjectAcceleratorFilter(project_id=project_id)
        )
        if accelerators:
            raise ProjectAcceleratorAlreadyExists(
                f"Accelerator for the project with id = {project_id.value} already exists."
            )
        user: User = self._user_read_repository.get_by_id(id_=user_id)
        project: Project = self._project_read_repository.get_by_id(id_=project_id)

        self._accelerator_service.create(
            user=user,
            project=project,
            payload=ProjectAcceleratorCreatePayload(
                project_id=project_id,
                name=command.name,
                description=command.description,
            ),
        )
        logger.info(f"Accelerator for the Project(id={project_id.value}) created successfully.")

    def update(self, user_id: Id, project_id: Id, command: ProjectAcceleratorUpdateCommand) -> None:
        """
        :raises UserNotFounException:
        :raises ProjectAcceleratorNotFoundException:
        :raises ProjectNotFoundException:
        """

        user: User = self._user_read_repository.get_by_id(id_=user_id)
        self._project_read_repository.get_by_id(id_=project_id)

        accelerators: list[ProjectAccelerator] = self._accelerator_read_repository.get_all(
            filter_=ProjectAcceleratorFilter(project_id=project_id)
        )
        if accelerators:
            logger.debug("User and Accelerator are exist.")
            self._accelerator_service.update(
                user=user,
                accelerator=accelerators[0],
                payload=ProjectAcceleratorUpdatePayload(
                    project_id=project_id, name=command.name, description=command.description
                ),
            )
        else:
            logger.exception(f"ProjectAccelerator doesn't exists for the Project(id={project_id.value})")
            raise ProjectAcceleratorNotFoundException(
                f"ProjectAccelerator for the project with id = {project_id.value} doesn't exists."
            )

    def delete(self, user_id: Id, project_id: Id) -> None:
        """
        :raises ProjectAcceleratorNotFoundException:
        :raises UserNotFoundException:
        """
        user: User = self._user_read_repository.get_by_id(id_=user_id)
        accelerators: list[ProjectAccelerator] = self._accelerator_read_repository.get_all(
            filter_=ProjectAcceleratorFilter(project_id=project_id)
        )
        if accelerators:
            self._accelerator_service.delete(user=user, accelerator=accelerators[0])
        else:
            logger.exception(f"ProjectAccelerator not found for the Project(id={project_id.value})")
            raise ProjectAcceleratorNotFoundException(
                f"Accelerator not found for the project with id = {project_id.value}"
            )
