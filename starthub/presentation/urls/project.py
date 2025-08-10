from django.urls import path
from presentation.views.accelerator import AcceleratorView
from presentation.views.crowdfunding import CrowdfundingView
from presentation.views.project import MeProjectView, ProjectImageView, ProjectPlanView, ProjectSearchView, ProjectView

urlpatterns = [
    path("", ProjectView.as_view(), name="projects"),
    path("me/", MeProjectView.as_view(), name="me_projects"),
    path("search/", ProjectSearchView.as_view(), name="search_projects"),
    path("<int:project_id>/plan/", ProjectPlanView.as_view()),
    path("<int:project_id>/", ProjectView.as_view()),
    path("<int:project_id>/images/", ProjectImageView.as_view()),
    path("<int:project_id>/images/<int:image_order>", ProjectImageView.as_view()),
    path("accelerators/<int:accelerator_id>/", AcceleratorView.as_view()),
    path("crowdfundings/<int:project_id>/", CrowdfundingView.as_view()),
]
