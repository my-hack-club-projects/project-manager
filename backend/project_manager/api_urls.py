# # project_manager/urls.py
# from django.urls import path
# from .views_old import *

# urlpatterns = [
#     path('categories/', UserCategoriesAPIView.as_view(), name='user-categories'),
#     path('categories/<int:pk>/projects/', CategoryProjectsAPIView.as_view(), name='category-projects'),
#     path('projects/<int:pk>/taskcontainers/', ProjectTaskContainersAPIView.as_view(), name='project-task-containers'),
#     path('projects/<int:pk>/sessions/', ProjectSessionsAPIView.as_view(), name='project-sessions'),
#     path('sessions/<int:pk>/notes/', SessionNotesAPIView.as_view(), name='session-notes'),
#     path('taskcontainers/<int:pk>/tasks/', TaskContainerTasksAPIView.as_view(), name='task-container-tasks'),
#     # old endpoints above, bad structure
#     # writing new ones below
#     # the structure should be: GET resource/identifier/ that returns a json of the resource, serialized
#     # POST resource/ that creates a new resource
#     # PUT, DELETE resource/identifier/ that updates or deletes the resource
# ]

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ProjectViewSet, TaskContainerViewSet, SessionViewSet, TaskViewSet

# Create a router and register our viewsets with it.
router = DefaultRouter()

# Categories
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'taskcontainers', TaskContainerViewSet, basename='taskcontainer')
router.register(r'sessions', SessionViewSet, basename='session')
router.register(r'tasks', TaskViewSet, basename='task')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]