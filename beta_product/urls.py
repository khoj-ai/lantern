from django.urls import path
from .views import (
    UserInterestListApiView,
)

urlpatterns = [
    path('users/', UserInterestListApiView.as_view()),
]