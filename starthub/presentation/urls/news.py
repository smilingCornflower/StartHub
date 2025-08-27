from django.urls import path
from presentation.views.news import NewsActivateView, NewsDeactivateView, NewsTagView, NewsView

urlpatterns = [
    path("", NewsView.as_view()),
    path("<int:news_id>/", NewsView.as_view()),
    path("<int:news_id>/activate/", NewsActivateView.as_view()),
    path("<int:news_id>/deactivate/", NewsDeactivateView.as_view()),
    path("<int:news_id>/tags/", NewsTagView.as_view()),
    path("<int:news_id>/tags/<str:tag_name>/", NewsTagView.as_view()),
]
