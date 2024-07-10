# project_manager/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.http import Http404
from .models import *
from .serializers import *

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
        "name": "New Project"
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

        if category.locked:
            return Response({"error": "Cannot create a project in a locked category."}, status=status.HTTP_403_FORBIDDEN)
        
        data = request.data
        data['category'] = category.id  # Assign category ID to the project data
        serializer = ProjectSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectTaskContainersAPIView(APIView):
    """
    Retrieve task containers within a specific project or create a new task container in the project.

    GET:
    Retrieve a list of task containers within a specific project.

    POST:
    Create a new task container in the project.

    PUT:
    Rename a task container. You can not mark a task container as completed or change any of the other properties.

    Example POST data:
    {
        "title": "New Task Container",
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

        if project.category.locked:
            return Response({"error": "Cannot create a task container in a locked project."}, status=status.HTTP_403_FORBIDDEN)
        
        request.data['project'] = project.id
        serializer = TaskContainerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        project = self.get_project(pk)

        if project.category.locked:
            return Response({"error": "Cannot update a task container in a locked project."}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            task_container = TaskContainer.objects.get(pk=request.data['id'], project=project)
        except TaskContainer.DoesNotExist:
            return Response({"error": "Task container does not exist."}, status=status.HTTP_404_NOT_FOUND)
        
        if not 'title' in request.data:
            return Response({"error": "Title is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            task_container.title = request.data['title']
        except ValueError:
            return Response({"error": "Invalid title."}, status=status.HTTP_400_BAD_REQUEST)
        
        task_container.save()

        serializer = TaskContainerSerializer(task_container)
        return Response(serializer.data)
    
class ProjectSessionsAPIView(APIView):
    """
    Retrieve sessions within a specific project or create a new session in the project.

    GET:
    Retrieve a list of sessions within a specific project.

    POST:
    Create a new session in the project. Only one session can be active at a time.

    Example POST data:
    {
        "duration": 60,
        "goal": "Work on this and that feature",
        "tasks": [1, 2, 3],  # List of task IDs that will be worked on during the session
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
        sessions = Session.objects.filter(project=project)
        serializer = SessionSerializer(sessions, many=True)
        return Response(serializer.data)
    
    def post(self, request, pk):
        # check if there is an active session for the user (because they can't be working on multiple projects at the same time)
        active_sessions = Session.objects.filter(project__category__user=self.request.user, active=True)

        if active_sessions.exists():
            return Response({"error": "There is already an active session for the user."}, status=status.HTTP_400_BAD_REQUEST)
        
        # check the tasks (if they belong to the project and are not completed)
        tasks = request.data.get('tasks', [])
        for task_id in tasks:
            try:
                task = Task.objects.get(pk=task_id)
                if task.is_completed:
                    return Response({"error": f"Task '{task.title}' is already completed."}, status=status.HTTP_400_BAD_REQUEST)
                elif task.task_container.project.id != pk:
                    return Response({"error": f"Task '{task.title}' does not belong to the project."}, status=status.HTTP_400_BAD_REQUEST)
            except Task.DoesNotExist:
                return Response({"error": f"Task with ID '{task_id}' does not exist."}, status=status.HTTP_404_NOT_FOUND)
            
        project = self.get_project(pk)

        if project.category.locked:
            return Response({"error": "Cannot create a session in a locked project."}, status=status.HTTP_403_FORBIDDEN)
        
        request.data['project'] = project.id
        serializer = SessionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskContainerTasksAPIView(APIView):
    """
    Retrieve tasks within a specific task container or create a new task in the task container.

    GET:
    Retrieve a list of tasks within a specific task container.

    POST:
    Create a new task in the task container.

    PUT:
    Mark a task as completed or change the title. You can not mark a task as incomplete or change any of the other properties.

    Example POST data:
    {
        "title": "New Task",
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

        if task_container.project.category.locked or task_container.is_completed:
            return Response({"error": "Cannot create a task in a locked task container."}, status=status.HTTP_403_FORBIDDEN)
        
        request.data['task_container'] = task_container.id
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        task_container = self.get_task_container(pk)

        if task_container.project.category.locked:
            return Response({"error": "Cannot update a task in a locked task container."}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            task = Task.objects.get(pk=request.data['id'], task_container=task_container)
        except Task.DoesNotExist:
            return Response({"error": "Task does not exist."}, status=status.HTTP_404_NOT_FOUND)
        
        if 'is_completed' in request.data:
            if task.is_completed:
                return Response({"error": "Task is already completed."}, status=status.HTTP_400_BAD_REQUEST)
            task.is_completed = True

            if not task_container.tasks.filter(is_completed=False).exists():
                task_container.is_completed = True
                task_container.save()
        if 'title' in request.data:
            try:
                task.title = request.data['title']
            except ValueError:
                return Response({"error": "Invalid title."}, status=status.HTTP_400_BAD_REQUEST)

        task.save()

        serializer = TaskSerializer(task)
        return Response(serializer.data)
    
class SessionNotesAPIView(APIView):
    """
    Retrieve notes within a specific session or create a new note in the session.

    GET:
    Retrieve a list of notes within a specific session.

    POST:
    Create a new note in the session.

    Example POST data:
    {
        "content": "This is a new note."
    }
    """
    permission_classes = [IsAuthenticated]

    def get_session(self, pk):
        try:
            return Session.objects.get(pk=pk, project__category__user=self.request.user)
        except Session.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        session = self.get_session(pk)
        notes = Note.objects.filter(session=session)
        serializer = NoteSerializer(notes, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        session = self.get_session(pk)

        if not session.active:
            return Response({"error": "Cannot create a note in an inactive session."}, status=status.HTTP_400_BAD_REQUEST)
        
        request.data['session'] = session.id
        request.data['user'] = request.user.id
        serializer = NoteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)