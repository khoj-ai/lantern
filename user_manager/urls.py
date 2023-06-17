from django.urls import path
from user_manager.views import UserDetailView, RegisterView

urlpatterns = [
    path("expand/", UserDetailView.as_view(), name="user-details"),
    path("onboard/", RegisterView.as_view(), name="auth-register"),
]
