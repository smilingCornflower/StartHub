from django.urls import path
from presentation.views.auth import AccessVerifyView, LoginView, RegistrationView, ReissueAccessTokenView

urlpatterns = [
    path("register/", RegistrationView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("reissue-access/", ReissueAccessTokenView.as_view(), name="reissue_access"),
    path("verify-access/", AccessVerifyView.as_view(), name="verify_access"),
]
