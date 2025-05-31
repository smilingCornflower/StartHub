from application.ports.service_factory import AbstractServiceFactory
from application.services.project import ProjectAppService
from domain.services.project import ProjectService
from domain.services.project_phone import ProjectPhoneService
from domain.services.project_social_link import ProjectSocialLinkService
from domain.services.team_member import TamMemberService
from infrastructure.repositories.company import DjCompanyReadRepository
from infrastructure.repositories.funding_model import DjFundingModelReadRepository
from infrastructure.repositories.project import DjProjectReadRepository, DjProjectWriteRepository
from infrastructure.repositories.project_category import DjProjectCategoryReadRepository
from infrastructure.repositories.project_phone import DjProjectPhoneReadRepository, DjProjectPhoneWriteRepository
from infrastructure.repositories.social_link import (
    DjProjectSocialLinkReadRepository,
    DjProjectSocialLinkWriteRepository,
)
from infrastructure.repositories.team_member import DjTeamMemberReadRepository, DjTeamMemberWriteRepository
from infrastructure.repositories.user import DjUserReadRepository


class ProjectServiceFactory(AbstractServiceFactory[ProjectAppService]):
    @staticmethod
    def create_service() -> ProjectAppService:
        return ProjectAppService(
            project_service=ProjectService(
                project_read_repository=DjProjectReadRepository(),
                project_write_repository=DjProjectWriteRepository(),
                project_category_read_repository=DjProjectCategoryReadRepository(),
                funding_model_read_repository=DjFundingModelReadRepository(),
                user_read_repository=DjUserReadRepository(),
                company_read_repository=DjCompanyReadRepository(),
            ),
            team_member_service=TamMemberService(
                team_member_read_repository=DjTeamMemberReadRepository(),
                team_member_write_repository=DjTeamMemberWriteRepository(),
            ),
            project_phone_service=ProjectPhoneService(
                project_phone_read_repository=DjProjectPhoneReadRepository(),
                project_phone_write_repository=DjProjectPhoneWriteRepository(),
            ),
            project_social_link_service=ProjectSocialLinkService(
                read_repository=DjProjectSocialLinkReadRepository(),
                write_repository=DjProjectSocialLinkWriteRepository(),
            ),
        )
