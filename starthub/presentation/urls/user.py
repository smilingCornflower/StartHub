from django.urls import path
from presentation.views.user import MeFavoriteProjectsView, MeView, UserView, UserFavoriteProjectsView

urlpatterns = [
    path("me/", MeView.as_view(), name="user_me"),

    path("<int:user_id>/", UserView.as_view(), name="user_detail"),

    path("<int:user_id>/favorites/", UserFavoriteProjectsView.as_view(), name="user_favorites"),

    path("me/favorites/", MeFavoriteProjectsView.as_view(), name="me_favorites"),

    path("me/favorites/<int:project_id>/", MeFavoriteProjectsView.as_view(), name="me_favorites_with_project_id"),
]
