# project_manager/urls.py
from django.urls import path
from .views import UserCategoriesAPIView, CategoryProjectsAPIView, ProjectTaskContainersAPIView, TaskContainerTasksAPIView

urlpatterns = [
    path('categories/', UserCategoriesAPIView.as_view(), name='user-categories'),
    path('categories/<int:pk>/projects/', CategoryProjectsAPIView.as_view(), name='category-projects'),
    path('projects/<int:pk>/taskcontainers/', ProjectTaskContainersAPIView.as_view(), name='project-task-containers'),
    path('taskcontainers/<int:pk>/tasks/', TaskContainerTasksAPIView.as_view(), name='task-container-tasks'),
    # Add more paths as needed for other views
]
