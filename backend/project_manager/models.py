from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    locked = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
class Project(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class TaskContainer(models.Model):
    title = models.CharField(max_length=200)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Task(models.Model):
    title = models.CharField(max_length=200)
    task_container = models.ForeignKey(TaskContainer, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Session(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    duration = models.IntegerField()  # in minutes
    active = models.BooleanField(default=True)
    goal = models.TextField()
    tasks = models.ManyToManyField(Task)

    def __str__(self):
        return f"Session for {self.project.name} at {self.start_time}"
