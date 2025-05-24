from django.urls import include, path

urlpatterns = [
    path("auth/", include("presentation.urls.auth")),
    path("foo/", include("presentation.urls.foo")),
]
