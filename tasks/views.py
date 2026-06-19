from django.db.models import Q
from rest_framework import generics, permissions
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Task
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
    return render(request,'tasks/task_list.html', {tasks : tasks,})