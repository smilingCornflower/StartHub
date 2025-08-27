from django.urls import include, path
from presentation.views.funding_model import FundingModelView
from presentation.views.geo import CityView, RegionView
from presentation.views.permission import PermissionView

urlpatterns = [
    path("auth/", include("presentation.urls.auth")),
    path("projects/", include("presentation.urls.project")),
    path("users/", include("presentation.urls.user")),
    path("news/", include("presentation.urls.news")),
    path("tests/", include("presentation.urls.test")),
    path("companies/", include("presentation.urls.company")),
    path("admin/", include("presentation.urls.admin")),
    path("cities/", CityView.as_view()),
    path("regions/", RegionView.as_view()),
    path("notifications/", include("presentation.urls.notification")),
    path("permissions/", PermissionView.as_view()),
    path("funding-models/", FundingModelView.as_view()),
]
