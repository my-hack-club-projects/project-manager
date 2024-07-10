# project_manager/urls.py
from django.urls import path
from .views import ProjectListCreateAPIView, TaskContainerListCreateAPIView, TaskContainerDetailAPIView, \
    TaskListCreateAPIView, TaskDetailAPIView, SessionListCreateAPIView

urlpatterns = [
    path('projects/', ProjectListCreateAPIView.as_view(), name='project-list-create'),
    path('taskcontainers/', TaskContainerListCreateAPIView.as_view(), name='task-container-list-create'),
    path('taskcontainers/<int:pk>/', TaskContainerDetailAPIView.as_view(), name='task-container-detail'),
    path('tasks/', TaskListCreateAPIView.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', TaskDetailAPIView.as_view(), name='task-detail'),
    path('sessions/', SessionListCreateAPIView.as_view(), name='session-list-create'),
    # Add more paths as needed for other views
]
