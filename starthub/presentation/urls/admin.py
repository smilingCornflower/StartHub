from django.urls import path
from presentation.views.admin import ProjectDeactivateView, ProjectSubmissionApproveView, ProjectSubmissionRejectedView

urlpatterns = [
    path("projects/submissions/<int:project_id>/approve/", ProjectSubmissionApproveView.as_view()),
    path("projects/submissions/<int:project_id>/reject/", ProjectSubmissionRejectedView.as_view()),
    path("projects/<int:project_id>/deactivate/", ProjectDeactivateView.as_view()),
]
