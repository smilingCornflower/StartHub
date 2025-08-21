from django.urls import path
from presentation.views.admin import ProjectSubmissionApproveView

urlpatterns = [
    path("project-submissions/<int:project_id>/approve/", ProjectSubmissionApproveView.as_view()),
]
