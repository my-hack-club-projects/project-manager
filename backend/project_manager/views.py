from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import Http404
from .models import Category, Project, TaskContainer, Session, Task
from .serializers import CategorySerializer, ProjectSerializer, TaskContainerSerializer, SessionSerializer, TaskSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    """
    GET /categories/
    POST /categories/
    PUT, DELETE /categories/<pk>/
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

class ProjectViewSet(viewsets.ModelViewSet):
    """
    GET /categories/<category_pk>/projects/
    POST /categories/<category_pk>/projects/
    PUT, DELETE /projects/<pk>/
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Project.objects.filter(category__user=self.request.user)

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        category_id = kwargs.get('category_pk')
        try:
            category = Category.objects.get(pk=category_id, user=request.user)
        except Category.DoesNotExist:
            raise Http404("Category does not exist")
        
        if category.locked:
            return Response({"error": "Cannot create a project in a locked category."}, status=status.HTTP_403_FORBIDDEN)

        data['category'] = category_id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class TaskContainerViewSet(viewsets.ModelViewSet):
    """
    GET /projects/<project_pk>/taskcontainers/
    POST /projects/<project_pk>/taskcontainers/
    PUT, DELETE /taskcontainers/<pk>/
    """
    queryset = TaskContainer.objects.all()
    serializer_class = TaskContainerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return TaskContainer.objects.filter(project__category__user=self.request.user)

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        project_id = kwargs.get('project_pk')
        try:
            project = Project.objects.get(pk=project_id, category__user=request.user)
        except Project.DoesNotExist:
            raise Http404("Project does not exist")
        
        if project.category.locked:
            return Response({"error": "Cannot create a task container in a locked project."}, status=status.HTTP_403_FORBIDDEN)

        data['project'] = project_id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.project.category.locked:
            return Response({"error": "Cannot update a task container in a locked project."}, status=status.HTTP_403_FORBIDDEN)
        
        if 'title' in request.data:
            if instance.is_completed:
                return Response({"error": "Cannot update the title of a completed task container."}, status=status.HTTP_403_FORBIDDEN)
            instance.title = request.data['title']
        
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class SessionViewSet(viewsets.ModelViewSet):
    """
    GET /projects/<project_pk>/sessions/
    POST /projects/<project_pk>/sessions/
    PUT, DELETE /sessions/<pk>/
    """
    queryset = Session.objects.all()
    serializer_class = SessionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Session.objects.filter(project__category__user=self.request.user)

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        project_id = kwargs.get('project_pk')
        try:
            project = Project.objects.get(pk=project_id, category__user=request.user)
        except Project.DoesNotExist:
            raise Http404("Project does not exist")
        
        if project.category.locked:
            return Response({"error": "Cannot create a session in a locked project."}, status=status.HTTP_403_FORBIDDEN)

        active_sessions = Session.objects.filter(project__category__user=self.request.user, active=True)
        if active_sessions.exists():
            return Response({"error": "There is already an active session for the user."}, status=status.HTTP_400_BAD_REQUEST)
        
        tasks = data.get('tasks', [])
        for task_id in tasks:
            try:
                task = Task.objects.get(pk=task_id)
                if task.is_completed or task.task_container.project.id != project_id:
                    return Response({"error": f"Invalid task ID '{task_id}'."}, status=status.HTTP_400_BAD_REQUEST)
            except Task.DoesNotExist:
                return Response({"error": f"Task with ID '{task_id}' does not exist."}, status=status.HTTP_404_NOT_FOUND)
        
        data['project'] = project_id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class TaskViewSet(viewsets.ModelViewSet):
    """
    GET /taskcontainers/<task_container_pk>/tasks/
    POST /taskcontainers/<task_container_pk>/tasks/
    PUT, DELETE /tasks/<pk>/
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(task_container__project__category__user=self.request.user)

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        task_container_id = kwargs.get('task_container_pk')
        try:
            task_container = TaskContainer.objects.get(pk=task_container_id, project__category__user=request.user)
        except TaskContainer.DoesNotExist:
            raise Http404("Task Container does not exist")
        
        if task_container.project.category.locked or task_container.is_completed:
            return Response({"error": "Cannot create a task in a locked task container."}, status=status.HTTP_403_FORBIDDEN)

        data['task_container'] = task_container_id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.task_container.project.category.locked:
            return Response({"error": "Cannot update a task in a locked task container."}, status=status.HTTP_403_FORBIDDEN)
        
        if 'is_completed' in request.data:
            if instance.is_completed:
                return Response({"error": "Cannot update a completed task."}, status=status.HTTP_400_BAD_REQUEST)
            instance.is_completed = True
            instance.save()
            
            task_container_tasks = Task.objects.filter(task_container=instance.task_container)
            if all([task.is_completed for task in task_container_tasks]):
                instance.task_container.is_completed = True
                instance.task_container.save()
        
        elif 'title' in request.data:
            return Response({"error": "Cannot update the title of a task."}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.task_container.project.category.locked:
            return Response({"error": "Cannot delete a task in a locked task container."}, status=status.HTTP_403_FORBIDDEN)
        
        instance.delete()
        return Response({"message": "Task deleted.", "success": True})