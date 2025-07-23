from django.urls import path
from presentation.views.test import TestView

urlpatterns = [
    path("", TestView.as_view(), name="test"),
]
