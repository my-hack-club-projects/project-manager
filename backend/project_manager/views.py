from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import Http404
from .models import Category, Project, TaskContainer, Task, Session 
from .serializers import CategorySerializer, ProjectSerializer, TaskContainerSerializer, TaskSerializer, SessionSerializer

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
        queryset = TaskContainer.objects.filter(project__category__user=self.request.user)
        project_id = self.request.query_params.get('project', None)
        if project_id is not None:
            queryset = queryset.filter(project_id=project_id)
        return queryset

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        
        try:
            project_id = data.get('project')
            project = Project.objects.get(pk=project_id, category__user=request.user)
        except Project.DoesNotExist:
            return Response({
                "success": False,
                "message": "Project does not exist."
            }, status=status.HTTP_404_NOT_FOUND)
        
        if project.category.locked:
            return Response({
                "success": False,
                "message": "Cannot create a task container in a locked project."
            }, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response({
            "success": True,
            "message": "Task container created successfully.",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.project.category.locked:
            return Response({
                "success": False,
                "message": "Cannot update a task container in a locked project."
            }, status=status.HTTP_403_FORBIDDEN)
        
        if 'title' in request.data:
            if instance.is_completed:
                return Response({
                    "success": False,
                    "message": "Cannot update the title of a completed task container."
                }, status=status.HTTP_403_FORBIDDEN)
            
            instance.title = request.data['title']
        
        instance.save()
        serializer = self.get_serializer(instance)
        
        return Response({
            "success": True,
            "message": "Task container updated successfully.",
            "data": serializer.data
        })
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.project.category.locked:
            return Response({
                "success": False,
                "message": "Cannot delete a task container in a locked project."
            }, status=status.HTTP_403_FORBIDDEN)
        elif instance.is_completed:
            return Response({
                "success": False,
                "message": "Cannot delete a completed task container."
            }, status=status.HTTP_403_FORBIDDEN)
        
        instance.delete()

        return Response({
            "success": True,
            "message": "Task container deleted successfully."
        })
    
class TaskViewSet(viewsets.ModelViewSet):
    """
    GET, POST /tasks/
    GET /tasks/?task_container=<task_container_id>
    GET /tasks/<pk>/
    PUT, DELETE /tasks/<pk>/
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Task.objects.filter(task_container__project__category__user=self.request.user)
        task_container_id = self.request.query_params.get('task_container', None)
        if task_container_id is not None:
            queryset = queryset.filter(task_container_id=task_container_id)
        return queryset

    def create(self, request, *args, **kwargs):
        data = request.data.copy()

        try:
            task_container_id = data.get('task_container')
            task_container = TaskContainer.objects.get(pk=task_container_id, project__category__user=request.user)
        except TaskContainer.DoesNotExist:
            return Response({
                "success": False,
                "message": "Task container does not exist."
            }, status=status.HTTP_404_NOT_FOUND)
        
        if task_container.project.category.locked or task_container.is_completed:
            return Response({
                "success": False,
                "message": "Cannot create a task in a locked or completed task container."
            }, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response({
            "success": True,
            "message": "Task created successfully.",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.task_container.project.category.locked or instance.task_container.is_completed:
            return Response({
                "success": False,
                "message": "Cannot update a task in a locked or completed task container."
            }, status=status.HTTP_403_FORBIDDEN)
        elif instance.is_completed:
            return Response({
                "success": False,
                "message": "Cannot update a completed task."
            }, status=status.HTTP_403_FORBIDDEN)
        
        if 'is_completed' in request.data:
            instance.is_completed = True
            instance.save()
            
            task_container_tasks = Task.objects.filter(task_container=instance.task_container)
            if all([task.is_completed for task in task_container_tasks]):
                instance.task_container.is_completed = True
                instance.task_container.save()
        
        elif 'title' in request.data:
            instance.title = request.data['title']
            instance.save()
        
        serializer = self.get_serializer(instance)
        
        return Response({
            "success": True,
            "message": "Task updated successfully.",
            "data": serializer.data
        })

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.task_container.project.category.locked or instance.task_container.is_completed or instance.is_completed:
            return Response({
                "success": False,
                "message": "Cannot delete that is completed or in a locked or completed task container."
            }, status=status.HTTP_403_FORBIDDEN)
        
        instance.delete()
        
        return Response({
            "success": True,
            "message": "Task deleted successfully."
        })

class SessionViewSet(viewsets.ModelViewSet):
    """
    GET, POST /sessions/
    GET /sessions/<pk>/
    PUT, DELETE /sessions/<pk>/
    """
    queryset = Session.objects.all()
    serializer_class = SessionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Session.objects.filter(project__category__user=self.request.user)
        project_id = self.request.query_params.get('project', None)
        active = self.request.query_params.get('active', None)
        task_id = self.request.query_params.get('task', None)
        if project_id is not None:
            queryset = queryset.filter(project_id=project_id)
        if active is not None:
            active = active.lower() == 'true'
            queryset = queryset.filter(active=active)
        if task_id is not None:
            queryset = queryset.filter(tasks__id=task_id)
        return queryset
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.project.category.user != request.user:
            return Response({
                "success": False,
                "message": "Session does not exist."
            }, status=status.HTTP_404_NOT_FOUND)

        if instance.active:
            instance.update_active_status()
            instance.save()

        serializer = self.get_serializer(instance)

        return Response({
            "success": True,
            "message": "Session retrieved successfully.",
            "data": serializer.data
        })
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        for session in queryset:
            if session.active:
                session.update_active_status()
                session.save()

        sessions = []

        for session in queryset:
            serializer = self.get_serializer(session)
            sessions.append(serializer.data)

        return Response({
            "success": True,
            "message": "Sessions retrieved successfully.",
            "data": sessions
        })

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        
        try:
            project_id = data.get('project')
            project = Project.objects.get(pk=project_id, category__user=request.user)
        except Project.DoesNotExist:
            return Response({
                "success": False,
                "message": "Project does not exist."
            }, status=status.HTTP_404_NOT_FOUND)
        
        if project.category.locked:
            return Response({
                "success": False,
                "message": "Cannot create a session in a locked project."
            }, status=status.HTTP_403_FORBIDDEN)

        # Update active status of all sessions
        queryset = self.get_queryset()
        active_sessions = queryset.filter(active=True)

        for session in active_sessions:
            session.update_active_status()
            session.save()

        # Check if there still is an active session
        active_sessions = Session.objects.filter(project__category__user=self.request.user, active=True)
        if active_sessions.exists():
            return Response({
                "success": False,
                "message": "There is already an active session."
            }, status=status.HTTP_400_BAD_REQUEST)
        
        tasks = data.get('tasks', [])
        for task_id in tasks:
            try:
                task = Task.objects.get(pk=task_id)
                if task.is_completed:
                    return Response({
                        "success": False,
                        "message": "Cannot start a session with a completed task."
                    }, status=status.HTTP_400_BAD_REQUEST)
                elif task.task_container.project != project:
                    return Response({
                        "success": False,
                        "message": "Task does not belong to the project."
                    }, status=status.HTTP_400_BAD_REQUEST)
            except Task.DoesNotExist:
                return Response({
                    "success": False,
                    "message": "Task does not exist."
                }, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        return Response({
            "success": True,
            "message": "Session created successfully.",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.project.category.locked:
            return Response({
                "success": False,
                "message": "Cannot update a session in a locked project."
            }, status=status.HTTP_403_FORBIDDEN)
        
        try:
            instance.duration = request.data.get('duration', instance.duration)
        except ValueError:
            return Response({
                "success": False,
                "message": "Duration must be a number."
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            instance.goal = request.data.get('goal', instance.goal)
        except ValueError:
            return Response({
                "success": False,
                "message": "Goal must be a string."
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if str(request.data.get('active')).lower().strip() == "false": # So it can be a string or a boolean
            instance.active = False
            instance.save()
        elif request.data.get('active'):
            return Response({
                "success": False,
                "message": "Cannot manually set a session to active."
            }, status=status.HTTP_400_BAD_REQUEST)
        
        instance.save()
        serializer = self.get_serializer(instance)
        
        return Response({
            "success": True,
            "message": "Session updated successfully.",
            "data": serializer.data
        })
    
    def destroy(self, request, *args, **kwargs):
        return Response({
            "success": False,
            "message": "Sessions cannot be deleted directly."
        }, status=status.HTTP_403_FORBIDDEN)