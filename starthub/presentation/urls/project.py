from django.urls import path
from presentation.views.accelerator import AcceleratorView
from presentation.views.crowdfunding import CrowdfundingView
from presentation.views.government_grant import GovernmentGrantView
from presentation.views.investment import (
    ProjectInvestmentPhoneView,
    ProjectInvestmentSocialLinkView,
    ProjectInvestmentView,
)
from presentation.views.project import MeProjectView, ProjectImageView, ProjectPlanView, ProjectSearchView, ProjectView

urlpatterns = [
    path("", ProjectView.as_view(), name="projects"),
    path("me/", MeProjectView.as_view(), name="me_projects"),
    path("search/", ProjectSearchView.as_view(), name="search_projects"),
    path("<int:project_id>/plan/", ProjectPlanView.as_view()),
    path("<int:project_id>/", ProjectView.as_view()),
    path("<int:project_id>/images/", ProjectImageView.as_view()),
    path("<int:project_id>/images/<int:image_order>", ProjectImageView.as_view()),
    path("<int:project_id>/accelerators/", AcceleratorView.as_view()),
    path("<int:project_id>/crowdfundings/", CrowdfundingView.as_view()),
    # Investment
    path("<int:project_id>/investments/", ProjectInvestmentView.as_view()),
    path("<int:project_id>/investments/<int:investment_id>/", ProjectInvestmentView.as_view()),
    path("investments/<int:investment_id>/social-links/", ProjectInvestmentSocialLinkView.as_view()),
    path("investments/social-links/<int:social_link_id>/", ProjectInvestmentSocialLinkView.as_view()),
    path("investments/<int:investment_id>/phone/", ProjectInvestmentPhoneView.as_view()),
    # Government Grant
    path("<int:project_id>/government-grants/", GovernmentGrantView.as_view()),
    path("government-grants/<int:government_grant_id>/", GovernmentGrantView.as_view()),
]
