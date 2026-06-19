from django.urls import path
from .views import task_list_view


app_name = "task_web"

urlpatterns = [
    path("", task_list_view, name="task-list"),
]