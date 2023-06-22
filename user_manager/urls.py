from django.urls import path
import user_manager.views as views

urlpatterns = [
    path("expand/", views.UserDetailView.as_view(), name="user-details"),
    path("onboard/", views.RegisterView.as_view(), name="auth-register"),
    path("login/", views.UserLoginView.as_view(), name="auth-login"),
    path("logout/", views.UserLogoutView.as_view(), name="auth-logout"),
    path("check/", views.CheckValidCredentials.as_view(), name="auth-check"),
]
