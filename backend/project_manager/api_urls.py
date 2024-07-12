from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ProjectViewSet, TaskContainerViewSet, SessionViewSet, TaskViewSet, NoteViewSet

# Create a router and register our viewsets with it.
router = DefaultRouter()

# Categories
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'taskcontainers', TaskContainerViewSet, basename='taskcontainer')
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'sessions', SessionViewSet, basename='session')
router.register(r'notes', NoteViewSet, basename='note')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]