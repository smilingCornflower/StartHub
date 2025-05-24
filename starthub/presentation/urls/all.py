from django.urls import include, path

urlpatterns = [
    path("auth/", include("presentation.urls.auth")),
]
