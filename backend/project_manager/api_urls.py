from django.urls import path
from . import views

urlpatterns = [
    path('projects/', views.ProjectListCreateAPIView.as_view(), name='project-list-create'),
    path('taskcontainers/', views.TaskContainerListCreateAPIView.as_view(), name='taskcontainer-list-create'),
    path('taskcontainers/<int:pk>/', views.TaskContainerDetailAPIView.as_view(), name='taskcontainer-detail'),
    path('tasks/', views.TaskListCreateAPIView.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', views.TaskDetailAPIView.as_view(), name='task-detail'),
    path('sessions/', views.SessionListCreateAPIView.as_view(), name='session-list-create'),
    path('sessions/<int:pk>/', views.SessionDetailAPIView.as_view(), name='session-detail'),
]
