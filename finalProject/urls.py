from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("api/", include ("tasks.urls")),
    path("tasks/", include("tasks.web_urls")),
    path("accounts/", include("django.contrib.auth.urls")),
]