from rest_framework import serializers
from .models import Project, TaskContainer, Task, Session

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

class TaskContainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskContainer
        fields = '__all__'

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = '__all__'