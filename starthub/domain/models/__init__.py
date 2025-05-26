from importlib import import_module

User = import_module("domain.models.user").User
Company = import_module("domain.models.company").Company
CompanyAttribute = import_module("domain.models.company").CompanyAttribute
Country = import_module("domain.models.country").Country
FundingModel = import_module("domain.models.funding_model").FundingModel
Project = import_module("domain.models.project").Project
TeamMember = import_module("domain.models.project").TeamMember
ProjectCategory = import_module("domain.models.project_category").ProjectCategory

__all__ = ["User", "Company", "CompanyAttribute", "Country", "FundingModel", "Project", "TeamMember", "ProjectCategory"]
