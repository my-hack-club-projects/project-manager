from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Category, Project, TaskContainer, Task, Session, Note
from .serializers import CategorySerializer, ProjectSerializer, TaskContainerSerializer, TaskSerializer, SessionSerializer, NoteSerializer

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

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.category.locked and not 'category' in request.data:
            return Response({
                "success": False,
                "message": "Cannot update a project in a locked category."
            }, status=status.HTTP_403_FORBIDDEN)
        
        if 'name' in request.data:
            instance.name = request.data['name']
        if 'description' in request.data:
            instance.description = request.data['description']
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
        return Response(serializer.data)
    
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
    
    def update_instance(self, instance, data):
        if instance.project.category.locked:
            return Response({
                "success": False,
                "message": "Cannot update a task container in a locked project."
            }, status=status.HTTP_403_FORBIDDEN)
        
        if 'order' in data: # Allow order to be updated even if the task container is completed
            instance.order = data['order']
        
        if 'title' in data:
            if instance.is_completed:
                return Response({
                    "success": False,
                    "message": "Cannot update the title of a completed task container."
                }, status=status.HTTP_403_FORBIDDEN)
            
            instance.title = data['title']
        
        instance.save()
        serializer = self.get_serializer(instance)
        
        return Response({
            "success": True,
            "data": serializer.data
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
                "message": "Cannot create a task container in a locked project."
            }, status=status.HTTP_403_FORBIDDEN)
        
        if not 'order' in data:
            data['order'] = TaskContainer.objects.filter(project=project).count()

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        return self.update_instance(instance, request.data)
    
    @action(detail=False, methods=['put'], url_path='bulk_update')
    def update_multiple(self, request, *args, **kwargs):
        if not isinstance(request.data, list):
            return Response({
                "success": False,
                "message": "Data must be a list."
            }, status=status.HTTP_400_BAD_REQUEST)
        elif not all(isinstance(task_container_data, dict) for task_container_data in request.data):
            return Response({
                "success": False,
                "message": "Data must be a list of dictionaries."
            }, status=status.HTTP_400_BAD_REQUEST)
        elif not all(['id' in task_container_data for task_container_data in request.data]):
            return Response({
                "success": False,
                "message": "All task containers must have an id."
            }, status=status.HTTP_400_BAD_REQUEST)
        
        data = request.data.copy()
        return_data = []

        for task_container_data in data:
            try:
                task_container_id = task_container_data['id']
                task_container = TaskContainer.objects.get(pk=task_container_id)

                response = self.update_instance(task_container, task_container_data)
                if not response.data['success']:
                    return Response({
                        "success": False,
                        "message": response.data['message']
                    })
                return_data.append(response.data['data'])
            except TaskContainer.DoesNotExist:
                return Response({
                    "success": False,
                    "message": "Task container does not exist."
                }, status=status.HTTP_404_NOT_FOUND)
        
        return Response(return_data)
    
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
    
    def update_instance(self, instance, data):
        if instance.task_container.project.category.locked or instance.task_container.is_completed:
            return Response({
                "success": False,
                "message": "Cannot update a task in a locked or completed task container."
            }, status=status.HTTP_403_FORBIDDEN)
        
        if 'order' in data: # Allow order to be updated even if the task is completed
            instance.order = data['order']
        
        if 'is_completed' in data:
            instance.is_completed = True
            instance.save()

            task_container_tasks = Task.objects.filter(task_container=instance.task_container)
            if all([task.is_completed for task in task_container_tasks]):
                instance.task_container.is_completed = True
                instance.task_container.save()
        
        if 'title' in data:
            if instance.is_completed:
                return Response({
                    "success": False,
                    "message": "Cannot update a completed task."
                }, status=status.HTTP_403_FORBIDDEN)
            
            instance.title = data['title']
        
        instance.save()
        serializer = self.get_serializer(instance)
        
        return Response({
            "success": True,
            "data": serializer.data
        })

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
        
        if not 'order' in data:
            data['order'] = Task.objects.filter(task_container=task_container).count()

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        return self.update_instance(instance, request.data)
    
    @action(detail=False, methods=['put'], url_path='bulk_update')
    def update_multiple(self, request, *args, **kwargs):
        if not isinstance(request.data, list):
            return Response({
                "success": False,
                "message": "Data must be a list."
            }, status=status.HTTP_400_BAD_REQUEST)
        elif not all(isinstance(task_data, dict) for task_data in request.data):
            return Response({
                "success": False,
                "message": "Data must be a list of dictionaries."
            }, status=status.HTTP_400_BAD_REQUEST)
        elif not all(['id' in task_data for task_data in request.data]):
            return Response({
                "success": False,
                "message": "All tasks must have an id."
            }, status=status.HTTP_400_BAD_REQUEST)
        
        data = request.data.copy()
        return_data = []

        for task_data in data:
            try:
                task_id = task_data['id']
                task = Task.objects.get(pk=task_id)
            except Task.DoesNotExist:
                return Response({
                    "success": False,
                    "message": "Task does not exist."
                }, status=status.HTTP_404_NOT_FOUND)
            response = self.update_instance(task, task_data)
            print(response.data)
            if not response.data['success']:
                return Response({
                    "success": False,
                    "message": response.data['message']
                })
            return_data.append(response.data['data'])
        
        return Response(return_data)
        
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

        return Response(serializer.data)
    
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

        return Response(sessions)

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
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
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
        
        return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        return Response({
            "success": False,
            "message": "Sessions cannot be deleted directly."
        }, status=status.HTTP_403_FORBIDDEN)
    
class NoteViewSet(viewsets.ModelViewSet):
    """
    GET, POST /notes/
    GET /notes/?session=<session_id>
    GET /notes/<pk>/
    PUT, DELETE /notes/<pk>/
    """
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Note.objects.filter(session__project__category__user=self.request.user)
        session_id = self.request.query_params.get('session', None)
        if session_id is not None:
            queryset = queryset.filter(session_id=session_id)
        return queryset

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        
        try:
            session_id = data.get('session')
            session = Session.objects.get(pk=session_id, project__category__user=request.user)
        except Session.DoesNotExist:
            return Response({
                "success": False,
                "message": "Session does not exist."
            }, status=status.HTTP_404_NOT_FOUND)
        
        if not session.active:
            return Response({
                "success": False,
                "message": "Cannot create a note in an inactive session."
            }, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance.session.active:
            return Response({
                "success": False,
                "message": "Cannot update a note in an inactive session."
            }, status=status.HTTP_403_FORBIDDEN)
        
        try:
            instance.content = request.data.get('content', instance.content)
        except ValueError:
            return Response({
                "success": False,
                "message": "Content must be a string."
            }, status=status.HTTP_400_BAD_REQUEST)
        
        instance.save()
        serializer = self.get_serializer(instance)
        
        return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        # You can delete notes even if the session is inactive - privacy reasons
        instance = self.get_object()
        
        instance.delete()

        return Response({
            "success": True,
            "message": "Note deleted successfully."
        })