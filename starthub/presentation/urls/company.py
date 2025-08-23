from django.urls import path
from presentation.views.company import CompanyView

urlpatterns = [
    path("", CompanyView.as_view(), name="company"),
    path("<int:company_id>/", CompanyView.as_view(), name="company"),
]
