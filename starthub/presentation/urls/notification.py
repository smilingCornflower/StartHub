from django.urls import path
from presentation.views.notification import NotificationView

urlpatterns = [
    path("<int:target_user_id>/", NotificationView.as_view()),
]
