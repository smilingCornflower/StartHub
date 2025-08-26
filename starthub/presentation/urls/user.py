from django.urls import path
from presentation.views.user import MeFavoriteProjectsView, MeView, UserFavoriteProjectsView, UserProfileView
from presentation.views.user_message import MeUserMessageView, UserMessageView

urlpatterns = [
    path("<int:user_id>/", UserProfileView.as_view(), name="user-profile"),
    path("<int:user_id>/favorites/", UserFavoriteProjectsView.as_view(), name="user_favorites"),
    path("me/", MeView.as_view(), name="user_me"),
    path("me/favorites/", MeFavoriteProjectsView.as_view(), name="me_favorites"),
    path("me/favorites/<int:project_id>/", MeFavoriteProjectsView.as_view(), name="me_favorites_with_project_id"),
    path("me/messages/", MeUserMessageView.as_view()),
    path("messages/", UserMessageView.as_view()),
]
