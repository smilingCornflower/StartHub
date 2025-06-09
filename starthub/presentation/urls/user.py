from django.urls import path
from presentation.views.user import MeView, UserView

urlpatterns = [
    path("me/", MeView.as_view(), name="user_me"),
    path("<int:user_id>/", UserView.as_view(), name="user_detail"),
]
