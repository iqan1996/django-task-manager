from django.contrib import admin
from django.urls import path, include

from django.contrib.auth.views import LoginView
from tasks.forms import BootstrapAuthenticationForm

from django.views.generic import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("api/", include ("tasks.urls")),
    path("tasks/", include("tasks.web_urls")),
    path(
    "accounts/login/",
    LoginView.as_view(
        template_name="registration/login.html",
        authentication_form=BootstrapAuthenticationForm,
    ),
    name="login",
),
path("accounts/", include("django.contrib.auth.urls")),
path("", RedirectView.as_view(pattern_name="tasks_web:task-list", permanent=False)),
]