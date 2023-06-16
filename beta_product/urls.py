from django.urls import path
from beta_product import views

urlpatterns = [
    path("users/", views.UserInterestListApiView.as_view()),
]
