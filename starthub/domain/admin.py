from django.contrib import admin
from django_stubs_ext import monkeypatch
from domain.models.geo.country import Country
from domain.models.funding_model import FundingModel
from domain.models.news import News, NewsImage
from domain.models.project import Project, ProjectPhone, ProjectSocialLink, TeamMember
from domain.models.project_category import ProjectCategory
from domain.models.user import User
from domain.models.user_favorite import UserFavorite

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


@admin.register(ProjectPhone)
class ProjectPhoneAdmin(admin.ModelAdmin[ProjectPhone]):
    pass


@admin.register(ProjectSocialLink)
class ProjectSocialLinkAdmin(admin.ModelAdmin[ProjectSocialLink]):
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


@admin.register(UserFavorite)
class UserFavoriteAdmin(admin.ModelAdmin[UserFavorite]):
    pass


@admin.register(News)
class NewsAdmin(admin.ModelAdmin[News]):
    pass


@admin.register(NewsImage)
class NewsImageAdmin(admin.ModelAdmin[NewsImage]):
    pass
