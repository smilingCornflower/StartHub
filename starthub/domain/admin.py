from django.contrib import admin
from django_stubs_ext import monkeypatch
from domain.models.country import Country
from domain.models.funding_model import FundingModel
from domain.models.project import Project, TeamMember
from domain.models.project_category import ProjectCategory
from domain.models.user import User

monkeypatch()


@admin.register(User)
class UserAdmin(admin.ModelAdmin[User]):
    pass


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin[Project]):
    pass


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin[TeamMember]):
    pass


@admin.register(ProjectCategory)
class ProjectCategoryAdmin(admin.ModelAdmin[ProjectCategory]):
    pass


@admin.register(FundingModel)
class FundingModelAdmin(admin.ModelAdmin[FundingModel]):
    pass


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin[Country]):
    pass
