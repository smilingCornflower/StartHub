from importlib import import_module

User = import_module("domain.models.user").User
Country = import_module("domain.models.country").Country
FundingModel = import_module("domain.models.funding_model").FundingModel
Project = import_module("domain.models.project").Project
TeamMember = import_module("domain.models.project").TeamMember
ProjectSocialLink = import_module("domain.models.project").ProjectSocialLink
ProjectPhone = import_module("domain.models.project").ProjectPhone
ProjectPhoto = import_module("domain.models.project").ProjectPhoto
ProjectCategory = import_module("domain.models.project_category").ProjectCategory
Company = import_module("domain.models.company").Company
UserFavorite = import_module("domain.models.user_favorite").UserFavorite

__all__ = ["User", "Country", "FundingModel", "Project", "TeamMember", "ProjectCategory"]
