# from django.urls import reverse # DO NOT USE!!!
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from .models import Category, Project, TaskContainer, Task, Session

class ProjectManagerTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        self.category1 = Category.objects.create(user=self.user, name="Active Projects")
        self.category2 = Category.objects.create(user=self.user, name="Archived Projects", locked=True)

        self.project = Project.objects.create(category=self.category1, name="Test Project")

        self.task_container = TaskContainer.objects.create(project=self.project, title="Initial Task Container")

        self.task1 = Task.objects.create(task_container=self.task_container, title="First Task")
        self.task2 = Task.objects.create(task_container=self.task_container, title="Second Task")

        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_get_categories(self):
        response = self.client.get('/categories/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)
