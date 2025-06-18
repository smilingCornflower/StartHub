from importlib import import_module

User = import_module("domain.models.user").User
UserFavorite = import_module("domain.models.user_favorite").UserFavorite
Role = import_module("domain.models.role").Role
Permission = import_module("domain.models.permission").Permission

Project = import_module("domain.models.project").Project
Company = import_module("domain.models.company").Company
TeamMember = import_module("domain.models.project").TeamMember
ProjectPhone = import_module("domain.models.project").ProjectPhone
ProjectImage = import_module("domain.models.project").ProjectImage
ProjectSocialLink = import_module("domain.models.project").ProjectSocialLink
ProjectCategory = import_module("domain.models.project_category").ProjectCategory
FundingModel = import_module("domain.models.funding_model").FundingModel
Country = import_module("domain.models.country").Country

__all__ = [
    "User",
    "UserFavorite",
    "Role",
    "Permission",
    "Project",
    "Company",
    "TeamMember",
    "ProjectPhone",
    "ProjectImage",
    "ProjectSocialLink",
    "ProjectCategory",
    "FundingModel",
    "Country",
]
