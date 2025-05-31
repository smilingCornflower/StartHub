from django.urls import include, path

urlpatterns = [
    path("auth/", include("presentation.urls.auth")),
    path("project/", include("presentation.urls.project")),
    path("company/", include("presentation.urls.company")),
]
