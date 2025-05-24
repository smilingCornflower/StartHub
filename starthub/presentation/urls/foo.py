from django.urls import path
from presentation.views.foo import hello_view

urlpatterns = [path("", hello_view)]
