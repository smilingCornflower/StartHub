from domain.constants import PROJECT_IMAGES_MAX_AMOUNT
from domain.exceptions import BusinessRuleException
from domain.exceptions.cloud_storage import FileNotFoundCloudStorageException
from domain.exceptions.permissions import DeleteDeniedPermissionException, UpdateDeniedPermissionException
from domain.exceptions.project_management import (
    ProjectImageMaxAmountException,
    ProjectPhoneAlreadyExistsException,
    ProjectSocialLinkAlreadyExistsException,
)
from domain.models.project import Project, ProjectImage, ProjectPhone, ProjectSocialLink, TeamMember
from domain.ports.cloud_storage import AbstractCloudStorage
from domain.ports.service import AbstractDomainService
from domain.repositories.company import CompanyReadRepository, CompanyWriteRepository
from domain.repositories.project_management import (
    FundingModelReadRepository,
    ProjectCategoryReadRepository,
    ProjectImageReadRepository,
    ProjectImageWriteRepository,
    ProjectPhoneReadRepository,
    ProjectPhoneWriteRepository,
    ProjectReadRepository,
    ProjectSocialLinkReadRepository,
    ProjectSocialLinkWriteRepository,
    ProjectWriteRepository,
    TeamMemberReadRepository,
    TeamMemberWriteRepository,
)
from domain.repositories.user import UserReadRepository
from domain.services.file import PdfService
from domain.utils.path_provider import PathProvider
from domain.value_objects.cloud_storage import (
    CloudStorageCreateUrlPayload,
    CloudStorageDeletePayload,
    CloudStorageUploadPayload,
)
from domain.value_objects.common import Id, Order
from domain.value_objects.filter import ProjectFilter, ProjectImageFilter, ProjectPhoneFilter, ProjectSocialLinkFilter
from domain.value_objects.project_management import (
    ProjectCreatePayload,
    ProjectImageCreateCommand,
    ProjectImageCreatePayload,
    ProjectImageDeleteCommand,
    ProjectImageDeletePayload,
    ProjectImageUpdateCommand,
    ProjectImageUpdatePayload,
    ProjectPhoneCreatePayload,
    ProjectSocialLinkCreatePayload,
    ProjectUpdateCommand,
    ProjectUpdatePayload,
    TeamMemberCreatePayload,
)
from loguru import logger


class ProjectPhoneService(AbstractDomainService):
    def __init__(
        self,
        project_phone_read_repository: ProjectPhoneReadRepository,
        project_phone_write_repository: ProjectPhoneWriteRepository,
    ):
        self._read_repository = project_phone_read_repository
        self._write_repository = project_phone_write_repository

    def create(self, payload: ProjectPhoneCreatePayload) -> ProjectPhone:
        """:raises ProjectPhoneAlreadyExistsException:"""

        filter_result: list[ProjectPhone] = self._read_repository.get_all(
            ProjectPhoneFilter(project_id=payload.project_id, number=payload.number)
        )
        if filter_result:
            raise ProjectPhoneAlreadyExistsException(
                f"This phone number is already assigned to the project with id = {payload.project_id}"
            )
        return self._write_repository.create(payload)


class ProjectSocialLinkService(AbstractDomainService):
    def __init__(
        self,
        read_repository: ProjectSocialLinkReadRepository,
        write_repository: ProjectSocialLinkWriteRepository,
    ):
        self._read_repository = read_repository
        self._write_repository = write_repository

    def create(self, payload: ProjectSocialLinkCreatePayload) -> ProjectSocialLink:
        """:raises ProjectSocialLinkAlreadyExistsException:"""

        filter_result: list[ProjectSocialLink] = self._read_repository.get_all(
            ProjectSocialLinkFilter(project_id=payload.project_id, social_link=payload.social_link)
        )
        if filter_result:
            raise ProjectSocialLinkAlreadyExistsException(
                f"social_link: {payload.social_link} already exists for the project with id = {payload.project_id.value}."
            )
        return self._write_repository.create(payload)


class TamMemberService(AbstractDomainService):
    def __init__(
        self,
        team_member_read_repository: TeamMemberReadRepository,
        team_member_write_repository: TeamMemberWriteRepository,
    ):
        self._team_member_read_repository = team_member_read_repository
        self._team_member_write_repository = team_member_write_repository

    def create(self, payload: TeamMemberCreatePayload) -> TeamMember:
        return self._team_member_write_repository.create(payload)


class ProjectService(AbstractDomainService):
    def __init__(
        self,
        project_read_repository: ProjectReadRepository,
        project_write_repository: ProjectWriteRepository,
        project_category_read_repository: ProjectCategoryReadRepository,
        user_read_repository: UserReadRepository,
        funding_model_read_repository: FundingModelReadRepository,
        company_read_repository: CompanyReadRepository,
        company_write_repository: CompanyWriteRepository,
        cloud_storage: AbstractCloudStorage,
        pdf_service: PdfService,
    ):
        # TODO: cloud service and pdf_service violates domain & application logic. It is need to move these services to application layer
        self._project_read_repository = project_read_repository
        self._project_write_repository = project_write_repository
        self._project_category_read_repository = project_category_read_repository
        self._user_read_repository = user_read_repository
        self._funding_model_read_repository = funding_model_read_repository
        self._company_read_repository = company_read_repository
        self._company_write_repository = company_write_repository
        self._cloud_storage = cloud_storage
        self._pdf_service = pdf_service

    def get_by_id(self, id_: Id) -> Project:
        """:raises ProjectNotFoundException:"""
        return self._project_read_repository.get_by_id(id_=id_)

    def get(self, filter_: ProjectFilter) -> list[Project]:
        return self._project_read_repository.get_all(filter_=filter_)

    def get_plan_url(self, project_id: Id) -> str:
        plan_path = PathProvider.get_project_plan_path(project_id)
        return self._cloud_storage.create_url(payload=CloudStorageCreateUrlPayload(file_path=plan_path))

    def create(self, payload: ProjectCreatePayload) -> Project:
        """
        :raises ProjectCategoryNotFoundException:
        :raises UserNotFoundException:
        :raises FundingModelNotFoundException:
        :raises CompanyNotFoundException:
        :raises CompanyOwnershipRequiredException:
        """
        self._project_category_read_repository.get_by_id(payload.category_id)
        self._user_read_repository.get_by_id(payload.creator_id)
        self._funding_model_read_repository.get_by_id(payload.funding_model_id)

        project: Project = self._project_write_repository.create(payload)

        logger.info("Project created successfully.")
        project_plan_path: str = PathProvider.get_project_plan_path(Id(value=project.id))

        uploaded_path: str = self._cloud_storage.upload_file(
            CloudStorageUploadPayload(file_data=payload.plan_file.value, file_path=project_plan_path)
        )
        logger.debug("Project pdf uploaded.")

        assert project_plan_path == uploaded_path
        self._project_write_repository.update(
            ProjectUpdatePayload(id_=Id(value=project.id), plan_path=project_plan_path)
        )
        logger.debug("Project.plan field was updated.")

        return project

    def update(self, update_command: ProjectUpdateCommand) -> Project:
        """
        :raises ProjectNotFoundException:
        :raises UpdateDeniedPermissionException:
        :raises ProjectCategoryNotFoundException:
        :raises FundingModelNotFoundException:
        """
        project: Project = self._project_read_repository.get_by_id(update_command.project_id)
        if update_command.user_id.value != project.creator_id:
            raise UpdateDeniedPermissionException("User is not the creator of the project and cannot update it")

        if update_command.category_id:
            logger.debug("Checking category exists.")
            self._project_category_read_repository.get_by_id(update_command.category_id)

        if update_command.funding_model_id:
            logger.debug("Checking funding model exists.")
            self._funding_model_read_repository.get_by_id(update_command.funding_model_id)

        if update_command.plan_file:
            logger.info("Updating project_plan file.")
            project_plan_path: str = PathProvider.get_project_plan_path(Id(value=project.id))
            uploaded_path: str = self._cloud_storage.upload_file(
                CloudStorageUploadPayload(file_data=update_command.plan_file.value, file_path=project_plan_path)
            )
            logger.debug(f"File uploaded, uploaded_path = {uploaded_path}.")

        if update_command.company:
            logger.info("Updating company fields.")
            self._company_write_repository.update(update_command.company)
            logger.info("Company data updated successfully.")

        updated_project: Project = self._project_write_repository.update(
            ProjectUpdatePayload(
                id_=update_command.project_id,
                name=update_command.name,
                category_id=update_command.category_id,
                funding_model_id=update_command.funding_model_id,
                stage=update_command.stage,
                goal_sum=update_command.goal_sum,
                deadline=update_command.deadline,
            )
        )
        return updated_project

    def delete(self, project_id: Id, user_id: Id) -> None:
        """
        :raises DeletePermissionDenied:
        """
        project: Project = self._project_read_repository.get_by_id(id_=project_id)
        if project.creator_id != user_id.value:
            raise DeleteDeniedPermissionException("Permission denied: Only project owners can delete projects")

        self._project_write_repository.delete_by_id(id_=project_id)


class ProjectImageService(AbstractDomainService):
    def __init__(
        self,
        project_image_read_repository: ProjectImageReadRepository,
        project_image_write_repository: ProjectImageWriteRepository,
        project_read_repository: ProjectReadRepository,
        cloud_storage: AbstractCloudStorage,
    ):
        # TODO: move cloud_storage to application layer
        self._project_image_read_repository = project_image_read_repository
        self._project_image_write_repository = project_image_write_repository
        self._project_read_repository = project_read_repository
        self._cloud_storage = cloud_storage

    def create(self, command: ProjectImageCreateCommand) -> ProjectImage:
        """
        :raises ProjectNotFoundException:
        :raises UpdateDeniedPermissionException:
        :raises ProjectImageMaxAmountException:
        :raises BusinessRuleException:
        """

        project: Project = self._project_read_repository.get_by_id(command.project_id)
        if project.creator_id != command.user_id.value:
            logger.debug(f"creator_id = {project.creator_id}; user_id = {command.user_id.value}")
            raise UpdateDeniedPermissionException("You don't have permission to add images to this project")

        image_count = self._project_image_read_repository.get_images_count_for_project(command.project_id)
        if image_count == PROJECT_IMAGES_MAX_AMOUNT:
            logger.exception("Images max amount reached.")
            raise ProjectImageMaxAmountException(f"Project images max limit is {PROJECT_IMAGES_MAX_AMOUNT}")

        if image_count > PROJECT_IMAGES_MAX_AMOUNT:
            logger.critical("Project images amount exceeds allowed max limit!")
            raise BusinessRuleException(f"Project images max limit is {PROJECT_IMAGES_MAX_AMOUNT}")

        img_path: str = PathProvider.get_project_image_path(command.project_id)
        uploaded_path: str = self._cloud_storage.upload_file(
            CloudStorageUploadPayload(file_data=command.image_file.value, file_path=img_path)
        )
        assert img_path == uploaded_path, "Expected and actual paths don't match."

        logger.debug("Project image uploaded.")
        project_image: ProjectImage = self._project_image_write_repository.create(
            ProjectImageCreatePayload(project_id=command.project_id, file_path=img_path, order=image_count + 1)
        )
        logger.debug("project_image created successfully.")

        return project_image

    def get_paths(self, project_id: Id) -> list[str]:
        project_images: list[ProjectImage] = self._project_image_read_repository.get_all(
            ProjectImageFilter(project_id=project_id)
        )
        return [i.file_path for i in project_images]

    def get_urls(self, project_id: Id) -> list[str]:
        """:raises ProjectNotFoundException:"""
        self._project_read_repository.get_by_id(project_id)

        project_images: list[ProjectImage] = self._project_image_read_repository.get_all(
            ProjectImageFilter(project_id=project_id)
        )
        project_images.sort(key=lambda x: x.order)
        image_urls: list[str] = list()
        for i in project_images:
            image_url: str = self._cloud_storage.create_url(CloudStorageCreateUrlPayload(file_path=i.file_path))
            image_urls.append(image_url)
        logger.debug(f"Found {len(image_urls)} urls")
        return image_urls

    def delete(self, command: ProjectImageDeleteCommand) -> None:
        """:raises DeleteDeniedPermissionException:"""
        project: Project = self._project_read_repository.get_by_id(command.project_id)

        if project.creator_id != command.user_id.value:
            raise DeleteDeniedPermissionException("You don't have permission to delete image from this project")

        project_image_lst: list[ProjectImage] = self._project_image_read_repository.get_all(
            ProjectImageFilter(project_id=command.project_id, image_order=command.image_order)
        )
        if project_image_lst:
            project_image: ProjectImage = project_image_lst[0]

            self._project_image_write_repository.delete(
                data=ProjectImageDeletePayload(project_id=command.project_id, image_order=command.image_order)
            )
            self.reorder_images(project_id=command.project_id)
            logger.debug("Image record deleted from the database")

            try:
                image_path = project_image.file_path
                logger.debug(f"Deleting file {image_path}")
                self._cloud_storage.delete_file(payload=CloudStorageDeletePayload(file_path=image_path))
                logger.debug("Image file deleted from the cloud storage")
            except FileNotFoundCloudStorageException:
                logger.info("File not found in cloud storage. Ignoring this exception.")

    def reorder_images(self, project_id: Id) -> None:
        images: list[ProjectImage] = self._project_image_read_repository.get_all(
            ProjectImageFilter(project_id=project_id)
        )
        for i, image in enumerate(images, start=1):
            if i != image.order:
                logger.debug(
                    f"project_image with id: {image.id} does not match with right order."
                    f"\tImage order: {image.order}, need: {i}."
                    f"\tStarted updating order."
                )
                self._project_image_write_repository.update(
                    ProjectImageUpdatePayload(image_id=Id(value=image.id), order=Order(value=i))
                )
                logger.debug("Image order updated successfully.")
        logger.info("Images order reorganized")

    def update(self, command: ProjectImageUpdateCommand) -> None:
        """
        :raises ProjectNotFoundException:
        :raises UpdateDeniedPermissionException:
        """
        project: Project = self._project_read_repository.get_by_id(command.project_id)

        if project.creator_id != command.user_id.value:
            raise UpdateDeniedPermissionException("You don't have permission to update images of this project")

        if command.new_order:
            images: list[ProjectImage] = self._project_image_read_repository.get_all(
                ProjectImageFilter(project_id=command.project_id)
            )
            images.sort(key=lambda x: x.order)

            for img, new_ord in zip(images, command.new_order):
                logger.debug(f"img_id = {img.id}, new_ord = {new_ord}")
                self._project_image_write_repository.update(
                    ProjectImageUpdatePayload(image_id=Id(value=img.id), order=new_ord)
                )
            logger.info("Order updated successfully.")
