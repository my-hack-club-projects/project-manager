from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import Http404
from .models import Category, Project, TaskContainer, Session, Task
from .serializers import CategorySerializer, ProjectSerializer, TaskContainerSerializer, SessionSerializer, TaskSerializer

"""
Strict rules for returning responses:
- Always return a Response object
- Always return a dictionary with a key "success" that is True or False
- Always return a dictionary with a key "message" that is a string

- Always return a 400 status code if the request is invalid
- Always return a 403 status code if the request is forbidden
- Always return a 404 status code if the resource does not exist
- Always return a 2XX status code if the request is successful.

- If creating a resource and it was successful, return it in the response under a key "data"
"""

class CategoryViewSet(viewsets.ModelViewSet):
    """
    GET /categories/
    GET /categories/<pk>/
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
    
    def create(self, request, *args, **kwargs):
        # Categories cannot be created by the user directly
        return Response({
            "success": False,
            "message": "Categories cannot be created directly."
        }, status=status.HTTP_403_FORBIDDEN)
    
    def update(self, request, *args, **kwargs):
        # Categories cannot be updated by the user directly
        return Response({
            "success": False,
            "message": "Categories cannot be updated directly."
        }, status=status.HTTP_403_FORBIDDEN)
    
    def destroy(self, request, *args, **kwargs):
        # Categories cannot be deleted by the user directly
        return Response({
            "success": False,
            "message": "Categories cannot be deleted directly."
        }, status=status.HTTP_403_FORBIDDEN)


class ProjectViewSet(viewsets.ModelViewSet):
    """
    GET /projects/
    POST /projects/
    GET /projects/<pk>/
    PUT, DELETE /projects/<pk>/
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Project.objects.filter(category__user=self.request.user)
        category_id = self.request.query_params.get('category', None)
        if category_id is not None:
            queryset = queryset.filter(category_id=category_id)
        return queryset

    def create(self, request, *args, **kwargs):
        data = request.data.copy()

        try:
            category_id = data.get('category')
            category = Category.objects.get(pk=category_id, user=request.user)
        except Category.DoesNotExist:
            return Response({
                "success": False,
                "message": "Category does not exist."
            }, status=status.HTTP_404_NOT_FOUND)
        
        if category.locked:
            return Response({
                "success": False,
                "message": "Cannot create a project in a locked category."
            }, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

        return Response({
            "success": True,
            "message": "Project created successfully.",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.category.locked and not 'category' in request.data:
            return Response({
                "success": False,
                "message": "Cannot update a project in a locked category."
            }, status=status.HTTP_403_FORBIDDEN)
        
        if 'name' in request.data:
            instance.name = request.data['name']
        if 'category' in request.data:
            try:
                category_id = request.data['category']
                category = Category.objects.get(pk=category_id, user=request.user)
                instance.category = category
            except Category.DoesNotExist:
                return Response({
                    "success": False,
                    "message": "Category does not exist."
                }, status=status.HTTP_404_NOT_FOUND)
        
        instance.save()
        serializer = self.get_serializer(instance)
        return Response({
            "success": True,
            "message": "Project updated successfully.",
            "data": serializer.data
        })
    
    def destroy(self, request, *args, **kwargs):
        # You can delete projects even if they are in a locked category
        instance = self.get_object()

        instance.delete()
        return Response({
            "success": True,
            "message": "Project deleted successfully."
        })
    
class TaskContainerViewSet(viewsets.ModelViewSet):
    """
    GET /taskcontainers/
    POST /taskcontainers/
    GET /taskcontainers/<pk>/
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