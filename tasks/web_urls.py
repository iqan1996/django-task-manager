from django.urls import path
from .views import task_list_view,task_create_view


app_name = "tasks_web"

urlpatterns = [
    path("", task_list_view, name="task-list"),
    path("create/",task_create_view, name= "task-create"),
]