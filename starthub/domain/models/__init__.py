from importlib import import_module

User = import_module("domain.models.user_management.user").User
UserFavorite = import_module("domain.models.user_management.user_favorite").UserFavorite
UserMessage = import_module("domain.models.user_management.message").UserMessage

Role = import_module("domain.models.role").Role
Permission = import_module("domain.models.permission").Permission

Project = import_module("domain.models.project_management.project").Project
TeamMember = import_module("domain.models.project_management.team_member").TeamMember
ProjectPhone = import_module("domain.models.project_management.phone").ProjectPhone
ProjectImage = import_module("domain.models.project_management.image").ProjectImage
ProjectSocialLink = import_module("domain.models.project_management.social_link").ProjectSocialLink
ProjectUsefulLink = import_module("domain.models.project_management.useful_link").ProjectUsefulLink
ProjectCategory = import_module("domain.models.project_management.category").ProjectCategory
ProjectStep = import_module("domain.models.project_management.step").ProjectStep
ProjectIncubator = import_module("domain.models.project_management.incubator").ProjectIncubator
ProjectAccelerator = import_module("domain.models.project_management.accelerator").ProjectAccelerator
ProjectCrowdfunding = import_module("domain.models.project_management.crowdfunding").ProjectCrowdfunding
ProjectInvestment = import_module("domain.models.project_management.investment").ProjectInvestment
ProjectInvestmentSocialLink = import_module("domain.models.project_management.investment").ProjectInvestmentSocialLink
ProjectInvestmentPhone = import_module("domain.models.project_management.investment").ProjectInvestmentPhone
ProjectGovernmentGrant = import_module("domain.models.project_management.government_grant").ProjectGovernmentGrant
ProjectBootstrap = import_module("domain.models.project_management.bootstrap").ProjectBootstrap
ProjectBankLoan = import_module("domain.models.project_management.bank_loan").ProjectBankLoan
ProjectFile = import_module("domain.models.project_management.project_file").ProjectFile
ProjectMedia = import_module("domain.models.project_management.media").ProjectMedia

FundingModel = import_module("domain.models.project_management.funding_model").FundingModel
Company = import_module("domain.models.company").Company
Country = import_module("domain.models.geo.country").Country

City = import_module("domain.models.geo.city").City
Region = import_module("domain.models.geo.region").Region
Address = import_module("domain.models.geo.address").Address

News = import_module("domain.models.news").News
NewsImage = import_module("domain.models.news").NewsImage

Notification = import_module("domain.models.notification").Notification

__all__ = [
    "User",
    "UserFavorite",
    "UserMessage",
    "Role",
    "Permission",
    "Project",
    "TeamMember",
    "ProjectPhone",
    "ProjectImage",
    "ProjectSocialLink",
    "ProjectUsefulLink",
    "ProjectCategory",
    "ProjectStep",
    "ProjectIncubator",
    "ProjectAccelerator",
    "ProjectCrowdfunding",
    "ProjectInvestment",
    "ProjectInvestmentSocialLink",
    "ProjectInvestmentPhone",
    "ProjectGovernmentGrant",
    "ProjectBootstrap",
    "ProjectBankLoan",
    "ProjectFile",
    "ProjectMedia",
    "FundingModel",
    "Company",
    "Country",
    "City",
    "Region",
    "Address",
    "News",
    "NewsImage",
    "Notification",
]
