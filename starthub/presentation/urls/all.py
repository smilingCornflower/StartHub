from django.urls import include, path

urlpatterns = [
    path("auth/", include("presentation.urls.auth")),
    path("projects/", include("presentation.urls.project")),
    path("users/", include("presentation.urls.user")),
]
