from django.urls import path
from khoj_service import views

urlpatterns = [
    path("", views.RedirectToKhojStaticAssets.as_view()),
]
