from django.urls import path
from presentation.views.auth import AccessVerifyView, LoginView, RegistrationView, ReissueAccessTokenView

urlpatterns = [
    path("register/", RegistrationView.as_view()),
    path("login/", LoginView.as_view()),
    path("reissue-access/", ReissueAccessTokenView.as_view()),
    path("verify-access/", AccessVerifyView.as_view()),
]
