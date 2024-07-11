# from django.urls import reverse # DO NOT USE!!!
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from .models import Category, Project, TaskContainer, Task, Session
import time

class ProjectManagerTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        self.category1 = Category.objects.create(user=self.user, name="Active Projects")
        self.category2 = Category.objects.create(user=self.user, name="Archived Projects", locked=True)

        self.project = Project.objects.create(category=self.category1, name="Test Project")

        self.task_container = TaskContainer.objects.create(project=self.project, title="Initial Task Container")

        self.task1 = Task.objects.create(task_container=self.task_container, title="First Task")
        self.task2 = Task.objects.create(task_container=self.task_container, title="Second Task")
        
        self.session = Session.objects.create(project=self.project)
        self.session.tasks.set([self.task1, self.task2])
        self.session.save()

        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    # Test categories
    def test_get_categories(self):
        response = self.client.get('/api/categories/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2) # Two categories that we created in setUp

    def test_create_category(self):
        response = self.client.post('/api/categories/', {
            'user': self.user.id,
            'name': 'New Category'
            })
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_category(self):
        response = self.client.put(f'/api/categories/{self.category1.id}/', {
            'user': self.user.id,
            'name': 'Updated Category'
            })
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_category(self):
        response = self.client.delete(f'/api/categories/{self.category1.id}/')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # Test projects
    def test_get_projects(self):
        response = self.client.get('/api/projects/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1) # One project that we created in setUp

    def test_get_projects_in_category(self):
        # use query params to filter projects in a category
        response = self.client.get(f'/api/projects/?category={self.category1.id}')
        count_from_db = Project.objects.filter(category=self.category1).count()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), count_from_db)

        response = self.client.get(f'/api/projects/?category={self.category2.id}')
        count_from_db = Project.objects.filter(category=self.category2).count()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), count_from_db)

    def test_create_delete_project(self):
        response = self.client.post('/api/projects/', {
            'category': self.category1.id,
            'name': 'New Project'
            })
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # remove the project we just created
        project_id = response.json()['data']['id']
        response = self.client.delete(f'/api/projects/{project_id}/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_move_project_to_archive(self):
        response = self.client.put(f'/api/projects/{self.project.id}/', {
            'category': self.category2.id,
            'name': 'Test Project'
            })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['data']['category'], self.category2.id)

    def test_move_project_from_archive(self):
        response = self.client.put(f'/api/projects/{self.project.id}/', {
            'category': self.category1.id,
            'name': 'Test Project'
            })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['data']['category'], self.category1.id)

    def test_rename_project(self):
        response = self.client.put(f'/api/projects/{self.project.id}/', { # move it first
            'category': self.category1.id
            })
        
        response = self.client.put(f'/api/projects/{self.project.id}/', {
            'name': 'Renamed Project'
            })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['data']['name'], 'Renamed Project')

    def test_rename_project_in_archive(self):
        response = self.client.put(f'/api/projects/{self.project.id}/', { # move it first
            'category': self.category2.id
            })
        
        response = self.client.put(f'/api/projects/{self.project.id}/', {
            'name': 'Renamed Project'
            })
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # Test task containers
    def test_get_task_containers(self):
        response = self.client.get('/api/taskcontainers/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1) # One task container that we created in setUp

    def test_get_task_containers_in_project(self):
        response = self.client.get(f'/api/taskcontainers/?project={self.project.id}')
        count_from_db = TaskContainer.objects.filter(project=self.project).count()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), count_from_db)

    def test_create_delete_task_container(self):
        response = self.client.post('/api/taskcontainers/', {
            'project': self.project.id,
            'title': 'New Task Container'
            })
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        response = self.client.delete(f'/api/taskcontainers/{response.json()["data"]["id"]}/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_rename_task_container(self):
        response = self.client.put(f'/api/taskcontainers/{self.task_container.id}/', {
            'title': 'Renamed Task Container'
            })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['data']['title'], 'Renamed Task Container')

    # Test tasks
    def test_get_tasks(self):
        response = self.client.get('/api/tasks/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2) # Two tasks that we created in setUp

    def test_get_tasks_in_task_container(self):
        response = self.client.get(f'/api/tasks/?task_container={self.task_container.id}')
        count_from_db = Task.objects.filter(task_container=self.task_container).count()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), count_from_db)

    def test_create_delete_task(self):
        response = self.client.post('/api/tasks/', {
            'task_container': self.task_container.id,
            'title': 'New Task'
            })
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        response = self.client.delete(f'/api/tasks/{response.json()["data"]["id"]}/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_rename_task(self):
        response = self.client.put(f'/api/tasks/{self.task1.id}/', {
            'title': 'Renamed Task'
            })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['data']['title'], 'Renamed Task')

    def test_complete_task(self):
        response = self.client.put(f'/api/tasks/{self.task1.id}/', {
            'is_completed': True
            })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['data']['is_completed'], True)

    # Test sessions
    def test_get_sessions(self):
        response = self.client.get('/api/sessions/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['data']), 1) # One session that we created in setUp

    def test_get_sessions_with_task(self):
        response = self.client.get(f'/api/sessions/?task={self.task1.id}')
        count_from_db = Session.objects.filter(tasks__exact=self.task1).count()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['data']), count_from_db)

    def test_create_delete_session(self):
        response = self.client.post('/api/sessions/', {
            'project': self.project.id,
            'tasks': [self.task2.id]
            })
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_session_w_complete_task(self):
        response = self.client.put(f'/api/tasks/{self.task1.id}/', {
            'is_completed': True
            })

        response = self.client.post('/api/sessions/', {
            'project': self.project.id,
            'tasks': [self.task1.id]
            })
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_stop_session(self):
        response = self.client.put(f'/api/sessions/{self.session.id}/', {
            'active': False
            })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['data']['active'], False)

    def test_attempt_delete_session(self):
        response = self.client.delete(f'/api/sessions/{self.session.id}/')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)