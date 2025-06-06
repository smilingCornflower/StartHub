from django.urls import path
from presentation.views.user import UserProfile

urlpatterns = [path("profile/", UserProfile.as_view())]
