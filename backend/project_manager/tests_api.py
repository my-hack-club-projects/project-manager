# project_manager/tests.py
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from .models import Category, Project, TaskContainer, Task, Session, Note

class ProjectManagerTests(APITestCase):

    def setUp(self):
        # Create a user and set password
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Create categories
        self.category1 = Category.objects.create(user=self.user, name="Active Projects")
        self.category2 = Category.objects.create(user=self.user, name="Archived Projects")

        # Create a project
        self.project = Project.objects.create(category=self.category1, name="Test Project")

        # Create a task container
        self.task_container = TaskContainer.objects.create(project=self.project, title="Initial Task Container")

        # Create tasks
        self.task1 = Task.objects.create(task_container=self.task_container, title="First Task")
        self.task2 = Task.objects.create(task_container=self.task_container, title="Second Task")

        # Get token for the user
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_get_user_categories(self):
        url = reverse('user-categories')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Should return the two categories

    def test_get_category_projects(self):
        url = reverse('category-projects', args=[self.category1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Should return one project

    def test_create_project_in_category(self):
        url = reverse('category-projects', args=[self.category1.id])
        data = {"name": "New Project"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Project.objects.count(), 2)  # Now there should be two projects

    def test_create_project_in_locked_category(self):
        url = reverse('category-projects', args=[self.category2.id])
        data = {"name": "New Project"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Project.objects.count(), 1)  # Should not create a project

    def test_get_project_task_containers(self):
        url = reverse('project-task-containers', args=[self.project.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Should return one task container

    def test_create_task_container_in_project(self):
        url = reverse('project-task-containers', args=[self.project.id])
        data = {"title": "New Task Container"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TaskContainer.objects.count(), 2)  # Now there should be two task containers

    def test_get_task_container_tasks(self):
        url = reverse('task-container-tasks', args=[self.task_container.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Should return two tasks

    def test_create_task_in_task_container(self):
        url = reverse('task-container-tasks', args=[self.task_container.id])
        data = {"title": "New Task"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 3)  # Now there should be three tasks

    def test_create_task_in_completed_task_container(self):
        # Mark the task container as completed
        self.task_container.is_completed = True
        self.task_container.save()

        url = reverse('task-container-tasks', args=[self.task_container.id])
        data = {"title": "New Task"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Task.objects.count(), 2)

    def test_get_project_sessions(self):
        url = reverse('project-sessions', args=[self.project.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_session_in_project(self):
        url = reverse('project-sessions', args=[self.project.id])
        data = {
            "duration": 60,
            "goal": "Work on feature X",
            "tasks": [self.task1.id, self.task2.id]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Session.objects.count(), 1)

    def test_get_session_notes(self):
        # Create a session
        session = Session.objects.create(project=self.project, duration=60, goal="Work on feature X", active=True)

        # Create notes
        Note.objects.create(session=session, user=self.user, content="First Note")
        Note.objects.create(session=session, user=self.user, content="Second Note")

        url = reverse('session-notes', args=[session.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Should return two notes

    def test_create_note_in_session(self):
        # Create a session
        session = Session.objects.create(project=self.project, duration=60, goal="Work on feature X", active=True)

        url = reverse('session-notes', args=[session.id])
        data = {"content": "This is a new note."}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Note.objects.count(), 1)
