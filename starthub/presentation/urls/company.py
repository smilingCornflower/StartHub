from django.urls import path
from presentation.views.company import CompanyView

urlpatterns = [path("", CompanyView.as_view())]
