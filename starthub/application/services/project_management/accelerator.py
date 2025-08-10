from application.ports.service import AbstractAppService
from domain.models.project_management.accelerator import ProjectAccelerator
from domain.models.user import User
from domain.repositories.project.accelerator import ProjectAcceleratorReadRepository
from domain.repositories.user import UserReadRepository
from domain.services.project_management.accelerator import ProjectAcceleratorService
from domain.value_objects.common import Id
from domain.value_objects.project.accelerator import AcceleratorId


class AcceleratorAppService(AbstractAppService):
    def __init__(
        self,
        read_repository: ProjectAcceleratorReadRepository,
        user_read_repository: UserReadRepository,
        accelerator_service: ProjectAcceleratorService,
    ):
        self._user_read_repository = user_read_repository
        self._read_repository = read_repository
        self._accelerator_service = accelerator_service

    def delete(self, user_id: Id, accelerator_id: AcceleratorId) -> None:
        """
        :raises ProjectAcceleratorNotFoundException:
        :raises UserNotFoundException:
        """
        user: User = self._user_read_repository.get_by_id(id_=user_id)
        accelerator: ProjectAccelerator = self._read_repository.get_by_id(id_=accelerator_id)
        self._accelerator_service.delete(user=user, accelerator=accelerator)
