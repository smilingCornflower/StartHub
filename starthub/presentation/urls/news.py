from django.urls import path
from presentation.views.news import NewsView

urlpatterns = [
    path("", NewsView.as_view()),
    path("<int:news_id>/", NewsView.as_view())
]
