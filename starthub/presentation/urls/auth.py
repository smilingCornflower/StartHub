from django.urls import path

from presentation.views.auth import (
    AccessVerifyView,
    GenerateAnonymousView,
    LoginView,
    LogoutView,
    RegistrationView,
    ReissueAccessTokenView,
    VerifyAnonymousView,
)

urlpatterns = [
    path("register/", RegistrationView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("reissue-access/", ReissueAccessTokenView.as_view(), name="reissue_access"),
    path("verify-access/", AccessVerifyView.as_view(), name="verify_access"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("generate-anonymous/", GenerateAnonymousView.as_view(), name="generate_anonymous"),
    path("verify-anonymous/", VerifyAnonymousView.as_view(), name="verify-anonymous"),
]
