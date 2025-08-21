from django.urls import path
from presentation.views.admin import ProjectSubmissionApproveView, ProjectSubmissionRejectedView

urlpatterns = [
    path("project-submissions/<int:project_id>/approve/", ProjectSubmissionApproveView.as_view()),
    path("project-submissions/<int:project_id>/reject/", ProjectSubmissionRejectedView.as_view()),
]
