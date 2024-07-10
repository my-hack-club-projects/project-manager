# project_manager/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.http import Http404
from .models import Category, Project, TaskContainer, Task
from .serializers import CategorySerializer, ProjectSerializer, TaskContainerSerializer, TaskSerializer

class UserCategoriesAPIView(APIView):
    """
    Retrieve categories for the authenticated user.

    GET:
    Retrieve a list of categories owned by the authenticated user.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        categories = Category.objects.filter(user=request.user)
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

class CategoryProjectsAPIView(APIView):
    """
    Retrieve projects within a specific category or create a new project in the category.

    GET:
    Retrieve a list of projects within a specific category.

    POST:
    Create a new project in the category.

    Example POST data:
    {
        "name": "New Project",
        "category": 1  # ID of the category
    }
    """
    permission_classes = [IsAuthenticated]

    def get_category(self, pk):
        try:
            return Category.objects.get(pk=pk, user=self.request.user)
        except Category.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        category = self.get_category(pk)
        projects = Project.objects.filter(category=category)
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        category = self.get_category(pk)
        request.data['category'] = category.id
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProjectTaskContainersAPIView(APIView):
    """
    Retrieve task containers within a specific project or create a new task container in the project.

    GET:
    Retrieve a list of task containers within a specific project.

    POST:
    Create a new task container in the project.

    Example POST data:
    {
        "title": "New Task Container",
        "project": 1  # ID of the project
    }
    """
    permission_classes = [IsAuthenticated]

    def get_project(self, pk):
        try:
            return Project.objects.get(pk=pk, category__user=self.request.user)
        except Project.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        project = self.get_project(pk)
        task_containers = TaskContainer.objects.filter(project=project)
        serializer = TaskContainerSerializer(task_containers, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        project = self.get_project(pk)
        request.data['project'] = project.id
        serializer = TaskContainerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskContainerTasksAPIView(APIView):
    """
    Retrieve tasks within a specific task container or create a new task in the task container.

    GET:
    Retrieve a list of tasks within a specific task container.

    POST:
    Create a new task in the task container.

    Example POST data:
    {
        "name": "New Task",
        "task_container": 1  # ID of the task container
    }
    """
    permission_classes = [IsAuthenticated]

    def get_task_container(self, pk):
        try:
            return TaskContainer.objects.get(pk=pk, project__category__user=self.request.user)
        except TaskContainer.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        task_container = self.get_task_container(pk)
        tasks = Task.objects.filter(task_container=task_container)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        task_container = self.get_task_container(pk)
        request.data['task_container'] = task_container.id
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
