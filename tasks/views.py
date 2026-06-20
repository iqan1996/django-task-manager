from django.db.models import Q
from rest_framework import generics, permissions
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required

from .models import Task
from .forms import TaskForm
from .serializers import TaskSerializer
from .permissions import IsOwnerOrReadOnly


class TaskListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Task.objects.all().order_by('-created_at')

        search_query = self.request.query_params.get('search')

        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query)
            )

        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TaskDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        return Task.objects.all()
    


@login_required
def task_list_view(request):
    tasks = Task.objects.all().select_related("owner").order_by("-created_at")
    return render(request,'tasks/task_list.html', {"tasks" : tasks,})

#for more safety ist better to write the code like this:

#from django.db.models import F
# @login_required
# def task_list_view(request):
#     tasks = (
#         Task.objects
#         .annotate(owner_username=F("owner__username"))
#         .values(
#             "id",
#             "title",
#             "description",
#             "created_at",
#             "owner_username",
#         )
#         .order_by("-created_at")
#     )
#     return render(request, "tasks/task_list.html", {"tasks": tasks})

@login_required
def task_create_view(request):
    if request.method == "POST":
        form = TaskForm(request.POST)


        if form.is_valid():
            task = form.save(commit=False)
            task.owner = request.user
            task.save()
            return redirect("tasks_web:task-list")
        
    else:
        form = TaskForm()

    return render(request, "tasks/task_form.html", {"form" : form})


