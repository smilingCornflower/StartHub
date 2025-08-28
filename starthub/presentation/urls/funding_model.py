from django.urls import path
from presentation.views.funding_model import FundingModelView

urlpatterns = [
    path("", FundingModelView.as_view()),
    path("<int:funding_model_id>/", FundingModelView.as_view()),
]
