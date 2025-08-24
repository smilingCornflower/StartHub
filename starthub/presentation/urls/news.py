from django.urls import path
from presentation.views.news import NewsActivateView, NewsDeactivateView, NewsView

urlpatterns = [
    path("", NewsView.as_view()),
    path("<int:news_id>/", NewsView.as_view()),
    path("<int:news_id>/activate/", NewsActivateView.as_view()),
    path("<int:news_id>/deactivate/", NewsDeactivateView.as_view()),
]
