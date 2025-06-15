from django.urls import path
from presentation.views.project import ProjectImageView, ProjectPlanView, ProjectView

urlpatterns = [
    path("", ProjectView.as_view()),
    path("<int:project_id>/plan/", ProjectPlanView.as_view()),
    path("<int:project_id>/", ProjectView.as_view()),
    path("<int:project_id>/images/", ProjectImageView.as_view()),
    path("<int:project_id>/images/<int:image_order>", ProjectImageView.as_view()),
]
