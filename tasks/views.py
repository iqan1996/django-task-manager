from django.db.models import Q
from rest_framework import generics, permissions
from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

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
    query = request.GET.get("q","").strip()
    tasks = Task.objects.all().select_related("owner").order_by("-created_at")

    if query:
        tasks = tasks.filter(
            Q(title__icontains = query) |
            Q(description__icontains=query)
        )

    return render(request,'tasks/task_list.html', {
        "tasks" : tasks,
        "query" : query})

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


@login_required
def task_detail_view(request, pk):
    task = get_object_or_404(Task.objects.select_related("owner"), pk=pk)

    return render(request, "tasks/task_detail.html", {"task":task,})


@login_required
def task_update_view(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if task.owner != request.user:
        raise PermissionDenied
    
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
    
        if form.is_valid():
            form.save()
            return redirect("tasks_web:task-detail", pk=task.pk)
        
    else:
        form = TaskForm(instance=task)
    
    return render(request, "tasks/task_form.html", {"form":form})


@login_required
def task_delete_view(request,pk):
    task = get_object_or_404(Task, pk=pk)

    if task.owner!=request.user:
        raise PermissionDenied
    
    if request.method == "POST":
        task.delete()
        return redirect("tasks_web:task-list")

    return render(request, "tasks/task_confirm_delete.html", {
        "task": task,
    })