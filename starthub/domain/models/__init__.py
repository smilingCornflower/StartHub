from importlib import import_module

User = import_module("domain.models.user").User
UserFavorite = import_module("domain.models.user_favorite").UserFavorite
Role = import_module("domain.models.role").Role
Permission = import_module("domain.models.permission").Permission

Project = import_module("domain.models.project_management.project").Project
TeamMember = import_module("domain.models.project_management.team_member").TeamMember
ProjectPhone = import_module("domain.models.project_management.phone").ProjectPhone
ProjectImage = import_module("domain.models.project_management.image").ProjectImage
ProjectSocialLink = import_module("domain.models.project_management.social_link").ProjectSocialLink
ProjectCategory = import_module("domain.models.project_management.category").ProjectCategory
ProjectStep = import_module("domain.models.project_management.step").ProjectStep
Company = import_module("domain.models.company").Company
FundingModel = import_module("domain.models.funding_model").FundingModel

Country = import_module("domain.models.geo.country").Country
Region = import_module("domain.models.geo.region").Region
City = import_module("domain.models.geo.city").City
Address = import_module("domain.models.geo.address").Address

News = import_module("domain.models.news").News
NewsImage = import_module("domain.models.news").NewsImage

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
    "Region",
    "City",
    "Address",
    "News",
    "NewsImage",
]
