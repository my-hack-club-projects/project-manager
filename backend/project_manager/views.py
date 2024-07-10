# project_manager/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.http import Http404
from .models import Project, TaskContainer, Task, Session
from .serializers import ProjectSerializer, TaskContainerSerializer, TaskSerializer, SessionSerializer

class ProjectListCreateAPIView(APIView):
    """
    List all projects or create a new project.

    GET:
    Retrieve a list of all projects.

    POST:
    Create a new project.

    Example POST data:
    {
        "name": "New Project"
    }
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        projects = Project.objects.filter(user=request.user)
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskContainerListCreateAPIView(APIView):
    """
    List all task containers or create a new task container.

    GET:
    Retrieve a list of all task containers.

    POST:
    Create a new task container.

    Example POST data:
    {
        "title": "New Task Container"
    }
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        task_containers = TaskContainer.objects.filter(user=request.user)
        serializer = TaskContainerSerializer(task_containers, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TaskContainerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskContainerDetailAPIView(APIView):
    """
    Retrieve, update or delete a task container instance.

    GET:
    Retrieve details of a specific task container.

    PUT:
    Update details of a specific task container.

    DELETE:
    Delete a specific task container.
    """
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return TaskContainer.objects.get(pk=pk, user=self.request.user)
        except TaskContainer.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        task_container = self.get_object(pk)
        serializer = TaskContainerSerializer(task_container)
        return Response(serializer.data)

    def put(self, request, pk):
        task_container = self.get_object(pk)
        serializer = TaskContainerSerializer(task_container, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        task_container = self.get_object(pk)
        task_container.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class TaskListCreateAPIView(APIView):
    """
    List all tasks or create a new task.

    GET:
    Retrieve a list of all tasks.

    POST:
    Create a new task.

    Example POST data:
    {
        "name": "New Task",
        "task_container": 1  # ID of the task container
    }
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tasks = Task.objects.filter(task_container__user=request.user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskDetailAPIView(APIView):
    """
    Retrieve, update or delete a task instance.

    GET:
    Retrieve details of a specific task.

    PUT:
    Update details of a specific task.

    DELETE:
    Delete a specific task.
    """
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Task.objects.get(pk=pk, task_container__user=self.request.user)
        except Task.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        task = self.get_object(pk)
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    def put(self, request, pk):
        task = self.get_object(pk)
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        task = self.get_object(pk)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class SessionListCreateAPIView(APIView):
    """
    List all sessions or create a new session.

    GET:
    Retrieve a list of all sessions.

    POST:
    Create a new session.

    Example POST data:
    {
        "duration": 60,
        "user": 1  # Replace with the authenticated user's ID
    }
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        sessions = Session.objects.filter(user=request.user)
        serializer = SessionSerializer(sessions, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SessionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
