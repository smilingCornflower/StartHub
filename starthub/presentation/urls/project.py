from django.urls import path
from presentation.views.accelerator import AcceleratorView
from presentation.views.bank_loan import ProjectBankLoanView
from presentation.views.bootstrap import ProjectBootstrapView
from presentation.views.crowdfunding import CrowdfundingView
from presentation.views.funding_model import ProjectCategoryView
from presentation.views.government_grant import GovernmentGrantView
from presentation.views.investment import (
    ProjectInvestmentPhoneView,
    ProjectInvestmentSocialLinkView,
    ProjectInvestmentView,
)
from presentation.views.metric import MetricView
from presentation.views.project import MeProjectView, ProjectImageView, ProjectPlanView, ProjectSearchView, ProjectView
from presentation.views.project_files import ProjectFileView
from presentation.views.project_media import ProjectMediaView
from presentation.views.project_useful_link import ProjectUsefulLinkView
from presentation.views.report import ProjectReportView
from presentation.views.resubmit import ProjectResubmitView

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
    # Bootstrap
    path("<int:project_id>/bootstraps/", ProjectBootstrapView.as_view()),
    path("bootstraps/<int:bootstrap_id>/", ProjectBootstrapView.as_view()),
    # Bank Loan
    path("<int:project_id>/bank-loans/", ProjectBankLoanView.as_view()),
    path("bank-loans/<int:bank_loan_id>/", ProjectBankLoanView.as_view()),
    # Metrics
    path("metrics/", MetricView.as_view()),
    # Files
    path("<int:project_id>/files/", ProjectFileView.as_view()),
    path("files/<int:project_file_id>/", ProjectFileView.as_view()),
    # Media
    path("<int:project_id>/media/", ProjectMediaView.as_view()),
    path("media/<int:project_media_id>/", ProjectMediaView.as_view()),
    # Useful Links
    path("<int:project_id>/useful_links/", ProjectUsefulLinkView.as_view()),
    path("useful_links/<int:useful_link_id>/", ProjectUsefulLinkView.as_view()),
    # Reports
    path("<int:project_id>/reports/", ProjectReportView.as_view()),
    # Resubmit
    path("<int:project_id>/resubmit/", ProjectResubmitView.as_view()),
    # Categories
    path("categories/", ProjectCategoryView.as_view()),
]
