# project_manager/views.py
from rest_framework import generics
from .models import Project, TaskContainer, Task, Session
from .serializers import ProjectSerializer, TaskContainerSerializer, TaskSerializer, SessionSerializer

class ProjectListCreateAPIView(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class TaskContainerListCreateAPIView(generics.ListCreateAPIView):
    queryset = TaskContainer.objects.all()
    serializer_class = TaskContainerSerializer

class TaskContainerDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TaskContainer.objects.all()
    serializer_class = TaskContainerSerializer

class TaskListCreateAPIView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class TaskDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class SessionListCreateAPIView(generics.ListCreateAPIView):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer

class SessionDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer
