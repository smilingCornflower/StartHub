from django.urls import path
from presentation.views.admin import (
    ProjectDeactivateView,
    ProjectSubmissionApproveView,
    ProjectSubmissionGetView,
    ProjectSubmissionRejectedView,
    UserAdminActivateView,
    UserAdminDeactivateView,
    UserDetailView,
    UsersAdminView,
)

urlpatterns = [
    path("projects/submissions/", ProjectSubmissionGetView.as_view()),
    path("projects/submissions/<int:project_id>/approve/", ProjectSubmissionApproveView.as_view()),
    path("projects/submissions/<int:project_id>/reject/", ProjectSubmissionRejectedView.as_view()),
    path("projects/<int:project_id>/deactivate_user/", ProjectDeactivateView.as_view()),
    path("users/", UserDetailView.as_view()),
    path("users/<int:target_user_id>/", UsersAdminView.as_view()),
    path("users/<int:target_user_id>/activate/", UserAdminActivateView.as_view()),
    path("users/<int:target_user_id>/deactivate/", UserAdminDeactivateView.as_view()),
]
