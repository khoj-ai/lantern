from django.urls import path
from beta_product import views

urlpatterns = [
    path("users/", views.UserInterestListApiView.as_view()),
    path("invite/<str:unique_identifier>/", views.UserInterestValidApiView.as_view()),
    path(
        "invite/<str:unique_identifier>/set-password/",
        views.InvitedUserSetPassword.as_view(),
    ),
]
