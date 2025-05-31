from django.urls import path
from presentation.views.project import ProjectView

urlpatterns = [path("", ProjectView.as_view()), path("<int:project_id>/", ProjectView.as_view())]
