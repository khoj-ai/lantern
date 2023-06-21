from django.urls import path
from khoj_service import views
from django.urls import re_path

urlpatterns = [
    path("", views.RedirectToKhojHomePage.as_view()),
    re_path(
        r".*/", views.RedirectToKhojAncilliaryAssets.as_view(), name="khoj_service"
    ),
]
