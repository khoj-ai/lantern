"""
URL configuration for lantern project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views
from django.urls import re_path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("beta/", include("beta_product.urls")),
    path("auth/", include("user_manager.urls")),
    path("token/", views.obtain_auth_token, name="token"),
    re_path(
        r"^api/chat/.*", include("khoj_service.api_urls"), name="khoj_service_chat"
    ),
    # api/chat/ is a special case, because the response needs to be streamed just for this endpoint.
    re_path(
        r"^api/chat.*", include("khoj_service.chat_urls"), name="khoj_service_chat"
    ),
    re_path(r"^api/.*", include("khoj_service.api_urls"), name="khoj_service_api"),
    path("", include("khoj_service.urls"), name="khoj_service"),
]
